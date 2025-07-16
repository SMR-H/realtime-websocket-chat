from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import *
from .forms import *


def home_view(request):
    return render(request, 'home.html')


@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            return Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            # Print email addresses with verification status
            print('\n=== Email Addresses ===')
            for email in request.user.emailaddress_set.all():
                print(f'Email: {email.email} | Verified: {email.verified}')

            print('=======================\n')
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                print(list(request.user.emailaddress_set.all()))
                # Print email addresses with verification status
                print('\n=== Email Addresses ===')
                for email in request.user.emailaddress_set.all():
                    print(f'Email: {email.email} | Verified: {email.verified}')
                print('=======================\n')
                messages.warning(request, 'You need to verify your email to join this group chat!')
                return redirect('profile-settings')

    if request.htmx:
        form = ChatmessageCreateForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'chat/partials/chat_message_p.html', context)
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chatroom_name': chatroom_name,
        'other_user': other_user,
        'chat_group': chat_group

    }
    return render(request, 'chat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = User.objects.get(username=username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)

    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form
    }
    return render(request, 'chat/new_groupchat.html', context)




