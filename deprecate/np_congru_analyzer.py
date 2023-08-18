# Standard
# None

# Pip
# None

# Custom
# None


def simple_congruency_check(morpho_results, np, np_article, article_codes):

    try:
        case = morpho_results.get("case").strip()
        np_data = morpho_results.get("np_data")
        tagged_data = dict()

        for row in np_data:
            # Leerzeilen nicht beachten
            split_data = [data for data in row.split(" ") if data]

            if len(split_data) == 2:
                word, tag = split_data
                tagged_data[tag] = word

        # DET and ADJ
        head = tagged_data.get("NN")
        article = tagged_data.get("DET", "ART")
        adj = tagged_data.get("ADJ")
        gender = morpho_results.get(head)[0][1]
        gender_code = np_article.get(gender).index(article)
        check_gender = bool(np_article.get(gender)[gender_code])

        # Genus und Kasus
        # Nom und Akk sind gleich, deswegen wird der Zeiger verschoben
        if gender == "fem" or "neut":
            check_case = article_codes.get(gender_code)
            if not check_case:
                move = 1
                check_case = article_codes.get(gender_code + move) == case
        else:
            check_case = article_codes.get(gender_code) == case

        check_adjective = False

        if adj:
            for row in morpho_results.get(adj):

                if gender in row and case in row:
                    check_adjective = True
        else:
            check_adjective = True

        checks = {"ADJ": check_adjective, "gender": check_gender, "case": check_case}

        correct_checks = 0

        for check in checks:
            value = checks.get(check)
            if value:
                correct_checks += 1

        if correct_checks == len(checks):
            np_data.append(1)
            return np_data
        else:
            np_data.append(0)
            return np_data

    except Exception as e:
        np_data.append(99)
        return np_data


if __name__ == "__main__":
    pass
