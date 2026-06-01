def keyword_overlap_score(text_list, target_text):
    score = 0
    target_text = target_text.lower()

    for text in text_list:
        words = str(text).lower().split()
        for word in words:
            if word in target_text:
                score += 1

    return score