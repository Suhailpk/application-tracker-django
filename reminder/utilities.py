def selecting_messaging_type(reminder_type, company_name, position):
    if reminder_type == "AP":
        message = '''Hi, Don't ever give up. Please follow the status of your company {company_name} as a {position}, and if possible, try
        to send a follow-up email to them.'''.format(company_name=company_name, position=position)
    elif reminder_type == "AA":
        message = '''Hello, Keep pushing forward! You are actively applying to companies like {company_name} for the position of {position}.
        Don't forget to track your progress and follow up when needed.'''.format(company_name=company_name, position=position)
    elif reminder_type == "SA":
        message = '''Hi, You're still applying for positions, including {company_name} as a {position}. Keep up the effort and continue reaching out!'''.format(company_name=company_name, position=position)
    elif reminder_type == "NS":
        message = '''Hello, Unfortunately, you weren't selected for the position at {company_name} as a {position}. Keep applying, better opportunities are ahead!'''.format(company_name=company_name, position=position)
    else:
        message = "Invalid reminder type."
    
    return message
