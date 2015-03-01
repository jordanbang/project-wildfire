from wildfire.models import Answer

def to_array(rep):
	options = []
	for i in xrange(1,6):
		option = rep.pop('option' + str(i))
		if option:
			options.append(option)
	return options


def to_columns(data):
	options = data.pop('options', None)
	if options and 'questionType' in data:
		question_type = data.get('questionType')
		# Need to update the options for either multiple choice or range values
		if question_type == 'MC' or question_type == 'RG':
			for i in xrange(0,5):
				if i < len(options) and options[i]:
					data['option' + str(i+1)] = options[i]
				else:
					data['option' + str(i+1)] = ""
		elif question_type == 'TF':
			data['option1'] = 'True'
			data['option2'] = 'False'
		elif question_type == 'RA':
			for i in xrange(1,6):
				data['option' + str(i)] = options[i-1]
	return data

def get_quick_stats(question_id):
	answers = Answer.objects.filter(question=question_id)
	return 	{
				'option1': answers.filter(answer = 0).count(),
				'option2': answers.filter(answer = 1).count(),
				'option3': answers.filter(answer = 2).count(),
				'option4': answers.filter(answer = 3).count(),
				'option5': answers.filter(answer = 4).count()
			}