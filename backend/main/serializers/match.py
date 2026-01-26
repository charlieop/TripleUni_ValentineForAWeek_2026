from rest_framework import serializers

class MatchResultSerializer(serializers.Serializer):
    """Serializer for GET:/match-result/<matchID> response"""

    def to_representation(self, instance):
        match = instance["match"]
        other_applicant = instance["other_applicant"]

        user_role = instance.get("user_role", 1)

        # Determine partner status
        user_status = (
            match.applicant1_status if user_role == 1 else match.applicant2_status
        )
        partner_status = (
            match.applicant2_status if user_role == 1 else match.applicant1_status
        )

        # Get partner head image path
        partner_head_image = None
        if other_applicant.wechat_info and other_applicant.wechat_info.head_image:
            partner_head_image = other_applicant.wechat_info.head_image.name

        # Get mentor qrcode path
        mentor_qrcode = None
        if match.mentor and match.mentor.wechat_qrcode:
            mentor_qrcode = match.mentor.wechat_qrcode.name

        nickname = (
            other_applicant.wechat_info.nickname
            if other_applicant.wechat_info
            else None
        )

        return {
            "partner_info": {
                "school": other_applicant.school,
                "grade": other_applicant.grade,
                "sex": other_applicant.sex,
                "mbti": {
                    "ei": other_applicant.mbti_ei,
                    "sn": other_applicant.mbti_sn,
                    "tf": other_applicant.mbti_tf,
                    "jp": other_applicant.mbti_jp,
                },
                "location": other_applicant.location,
                "message_to_partner": other_applicant.message_to_partner,
                "head_image": partner_head_image,
                "nickname": nickname,
            },
            "mentor_info": {
                "name": match.mentor.name,
                "wxid": match.mentor.wechat,
                "qrcode": mentor_qrcode,
            },
            "match_info": {
                "id": match.id,
                "round": match.round,
                "user_status": user_status,
                "partner_status": partner_status,
                "discarded": match.discarded,
                "discard_reason": match.discard_reason if match.discarded else None,
                
            },
        }


class MatchDetailSerializer(serializers.Serializer):
    """Serializer for GET:/match/<matchID> response"""

    def to_representation(self, instance):
        match = instance["match"]
        user_applicant = instance["user_applicant"]
        other_applicant = instance["other_applicant"]
        total_score = instance["total_score"]
        basic_complete = instance["basic_complete"]
        current_day = instance["current_day"]
        rank = instance["rank"]
        # Get user head image path
        user_head_image = None
        if user_applicant.wechat_info and user_applicant.wechat_info.head_image:
            user_head_image = user_applicant.wechat_info.head_image.name

        # Get partner head image path
        partner_head_image = None
        if other_applicant.wechat_info and other_applicant.wechat_info.head_image:
            partner_head_image = other_applicant.wechat_info.head_image.name

        # Get mentor qrcode path
        mentor_qrcode = None
        if match.mentor and match.mentor.wechat_qrcode:
            mentor_qrcode = match.mentor.wechat_qrcode.name

        return {
            "user_info": {
                "name": user_applicant.name,
                "head_image": user_head_image,
                "linked_uni": user_applicant.linked_uni,
            },
            "partner_info": {
                "name": other_applicant.name,
                "head_image": partner_head_image,
                "wxid": other_applicant.wxid,
            },
            "mentor_info": {
                "name": match.mentor.name,
                "wxid": match.mentor.wechat,
                "qrcode": mentor_qrcode,
            },
            "match_info": {
                "id": match.id,
                "name": match.name,
                "total_score": total_score,
                "basic_complete": basic_complete,
                "current_day": current_day,
                "rank": rank,
            },
        }
