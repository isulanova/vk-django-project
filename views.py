from django.shortcuts import render, redirect
from .models import User, FriendRequest


def list_friends(request):
    user = request.user
    friends = user.friends.all()
    context = {'friends': friends}
    return render(request, 'list_friends.html', context)


def list_incoming_requests(request):
    user = request.user
    requests = FriendRequest.objects.filter(to_users=user, status='0')
    context = {'requests': requests}
    return render(request, 'list_incoming_requests.html', context)


def list_outgoing_requests(request):
    user = request.user
    requests = FriendRequest.objects.filter(from_user=user, status='0')
    context = {'requests': requests}
    return render(request, 'list_outgoing_requests.html', context)


def send_friend_request(request, id):
    from_user = request.user
    to_user = User.objects.get(pk=id)
    FriendRequest.objects.create(from_user=from_user, to_users=to_user)
    return redirect('list_outgoing_requests')


def accept_friend_request(request, id):
    request = FriendRequest.objects.get(pk=id)
    request.accept()
    return redirect('list_friends')


def reject_friend_request(request, id):
    request = FriendRequest.objects.get(pk=id)
    request.reject()
    return redirect('list_incoming_requests')


def unfriend(request, id):
    user = request.user
    friend = User.objects.get(pk=id)
    user.friends.remove(friend)
    user.save()
    friend.friends.remove(user)
    friend.save()
    return redirect('list_friends')