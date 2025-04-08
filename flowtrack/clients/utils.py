from django.core.exceptions import ValidationError

def formatted_phone(phone):
    if phone:
        phone = ''.join(phone.split())
        if phone.startswith('+'):
            if phone[1:].isdigit():
                if len(phone) == 12:
                    return phone[:3] + " " + phone[3:5] + " " + phone[5:8] + " " + phone[8:10] + " " + phone [10: ]
                else:
                    raise ValidationError("Długość numeru jest niepoprawna")
        else:
            if phone.isdigit():
                if len(phone) == 9:
                    return ' '.join([phone[i:i+3] for i in range(0, len(phone), 3)])
                else:
                    raise ValidationError("Długość numeru jest niepoprawna")
            else:
                raise ValidationError("Numer telefonu może zawierać tylko cyfry lub znak '+' przy numerach kierunkowych")
    else:
        return ""
    
def formatted_nip(nip):
    if nip:
        if nip.isdigit():
            if len(nip) == 10:
                return nip
            else:
                raise ValidationError("Numer nip powinien mieć 10 cyfr")
        else:
            raise ValidationError("Nip może składać się wyłącznie z cyfr")
    else:
        return ""