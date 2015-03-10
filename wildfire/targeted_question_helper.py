from wildfire.models import Answer, TargetedQuestion, Question, UserProfile, Connected


#If a user answers a question, send that question to
#all of his connections
def target_from_answer(answer):
	for connection in Connected.objects.filter(user1=answer.user):
		print("Connection: " + str(connection.user2.id) + "    Answerer: " + str(answer.user.id))
		if TargetedQuestion.objects.filter(user=connection.user2, question=answer.question).count() == 0:
			target = TargetedQuestion(user=connection.user2, question=answer.question)
			target.save()

def target_from_question(question):
	for connection in Connected.objects.filter(user1=question.asker):
		target = TargetedQuestion(user=connection.user2, question=question)
		target.save()
