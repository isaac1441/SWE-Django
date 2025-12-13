from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import DirectConversation, Message

User = get_user_model()

@login_required
def inbox(request):
    convos = (DirectConversation.objects
              .filter(Q(user1=request.user) | Q(user2=request.user))
              .select_related("user1", "user2")
              .order_by("-created_at"))

    for c in convos:
        c.other = c.other_user(request.user)

    return render(request, "messaging/inbox.html", {"conversations": convos})

@login_required
def start_dm(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect("messaging:inbox")

    convo = DirectConversation.get_or_create_for_users(request.user, other)
    return redirect("messaging:thread", convo_id=convo.id)

@login_required
def thread(request, convo_id):
    convo = get_object_or_404(DirectConversation, id=convo_id)

    # Only participants can view
    if request.user.id not in (convo.user1_id, convo.user2_id):
        return redirect("messaging:inbox")

    other_user = convo.other_user(request.user)

    if request.method == "POST":
        body = (request.POST.get("body") or "").strip()
        if body:
            Message.objects.create(conversation=convo, sender=request.user, body=body)
        return redirect("messaging:thread", convo_id=convo.id)

    msgs = convo.messages.select_related("sender").all()
    return render(request, "messaging/thread.html", {
        "conversation": convo,
        "other_user": other_user,
        "messages": msgs,
    })
