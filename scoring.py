# scoring.py

def score_text_length(text, min_len=100, max_len=1200):
    if not text:
        return 0
    length = len(text.strip())
    if length < min_len:
        return 20
    if length > max_len:
        return 70
    return 100


def keyword_score(text, keywords):
    if not text:
        return 0
    text_lower = text.lower()
    matches = sum(1 for word in keywords if word in text_lower)
    return min(matches * 20, 100)


def score_leadership(leadership_experience, achievements):
    leadership_keywords = [
        "организовал", "руководил", "лидер", "команда",
        "инициировал", "создал", "запустил", "координировал"
    ]
    score1 = keyword_score(leadership_experience, leadership_keywords)
    score2 = keyword_score(achievements, ["проект", "олимпиада", "конкурс", "клуб", "волонтер"])
    return round((score1 * 0.6 + score2 * 0.4), 1)


def score_growth(growth_story):
    growth_keywords = [
        "преодолел", "научился", "ошибка", "опыт",
        "развился", "стал лучше", "смог", "изменился"
    ]
    base = keyword_score(growth_story, growth_keywords)
    length_bonus = score_text_length(growth_story, 80, 800) * 0.2
    return round(min(base + length_bonus, 100), 1)


def score_motivation(motivation_text, future_goals):
    motivation_keywords = [
        "развитие", "обучение", "помогать", "влияние",
        "общество", "лидерство", "изменения", "цель"
    ]
    score1 = keyword_score(motivation_text, motivation_keywords)
    score2 = keyword_score(future_goals, ["проект", "сообщество", "стартап", "изменить", "создать"])
    return round((score1 * 0.7 + score2 * 0.3), 1)


def score_initiative(achievements, volunteering):
    keywords = [
        "волонтер", "мероприятие", "организовал",
        "участвовал", "инициатива", "помогал", "собрал"
    ]
    score1 = keyword_score(achievements, keywords)
    score2 = keyword_score(volunteering, keywords)
    return round((score1 * 0.5 + score2 * 0.5), 1)


def score_clarity(essay_text):
    return round(score_text_length(essay_text, 150, 1500), 1)


def generate_explanation(scores):
    reasons = []

    if scores["leadership"] >= 70:
        reasons.append("есть выраженные сигналы лидерского потенциала")
    if scores["growth"] >= 70:
        reasons.append("хорошо описана траектория роста и преодоления трудностей")
    if scores["motivation"] >= 70:
        reasons.append("видна сильная и осознанная мотивация")
    if scores["initiative"] >= 70:
        reasons.append("есть признаки самостоятельной инициативы и участия в проектах")
    if scores["clarity"] < 50:
        reasons.append("текстовая часть раскрыта слабо, нужен ручной просмотр")

    if not reasons:
        reasons.append("профиль требует дополнительной ручной оценки")

    return "; ".join(reasons)


def calculate_candidate_score(candidate):
    leadership = score_leadership(
        candidate.get("leadership_experience", ""),
        candidate.get("achievements", "")
    )
    growth = score_growth(candidate.get("growth_story", ""))
    motivation = score_motivation(
        candidate.get("motivation_text", ""),
        candidate.get("future_goals", "")
    )
    initiative = score_initiative(
        candidate.get("achievements", ""),
        candidate.get("volunteering", "")
    )
    clarity = score_clarity(candidate.get("essay_text", ""))

    final_score = round(
        leadership * 0.30 +
        growth * 0.25 +
        motivation * 0.20 +
        initiative * 0.15 +
        clarity * 0.10,
        1
    )

    if final_score >= 75:
        recommendation = "Shortlist"
    elif final_score >= 55:
        recommendation = "Manual Review"
    else:
        recommendation = "Low Priority"

    scores = {
        "leadership": leadership,
        "growth": growth,
        "motivation": motivation,
        "initiative": initiative,
        "clarity": clarity,
        "final_score": final_score,
        "recommendation": recommendation
    }

    scores["explanation"] = generate_explanation(scores)
    return scores