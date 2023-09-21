"""
Script started by Imge Yüzüncüoglu, Raha Musavi in summer semester 2023 in the course
"Korpuslinguistische Analyse der Nominalflextion im Deutschen"
edited by Ronja Laarmann-Quante

last modified: 2023_08_10 by RLQ
"""
# modules to import
import pandas as pd
import pprint


def main_conll_to_pylist(infile, outfile):

    # list to store ALL nps of ONE FILE in
    nps_of_file = list()

    sentence_counter = 1
    np_counter = 1

    # open the file in read-mode
    try:
        with open(infile, "r", encoding="utf-8") as file:
            # read in the lines of token
            file_input = file.readlines()
    except UnicodeDecodeError:
        with open(infile, "r", encoding="utf-8-sig") as file:
            # read in the lines of token
            file_input = file.readlines()

    # list to generate a single sentences out of the file
    single_sentence = list()

    # go through each line/"sentence" of the file
    for lineindex, line in enumerate(file_input):
        # if it is not an empty line/"sentence", add it to the
        # list of a single sentence
        if line not in ["\n", "\r\n"]:
            single_sentence.append(line)

        # empty line/"sentence" indicates the end of a sentence
        if line in ["\n", "\r\n"] or lineindex == len(file_input) - 1:
            # split each element of the sentence into the single token-information
            sentence_as_elements = list()
            for row in single_sentence:
                elements = row.split("\t")
                sentence_as_elements.append(elements)

            # create dataframe with column names
            df = pd.DataFrame(
                sentence_as_elements,
                columns=[
                    "ID",
                    "token",
                    "lemma",
                    "wordtype",
                    "POSTag",
                    "features",
                    "head",
                    "deprel",
                    "dunno1",
                    "dunno2",
                ],
            )

            # delete columns we do not need
            df = df.drop(["dunno1", "dunno2"], axis=1)

            # extract the whole token-column to get the whole sentence as tokens
            sentence_list = df["token"].txt_id_dta.tolist()
            sentence_as_string = " ".join(sentence_list)
            number_of_tokens_of_sentence = len(sentence_list)

            token_head_list = list()

            token_index_list = list()

            token_id_list = list()

            # generate lists of heads
            # go through the dataframe of the file
            for index, row in df.iterrows():
                token_head_list.append([[row["token"]], row["head"]])

                # add the token and its index to the other list
                token_index_list.append([[row["token"]], index])
                token_id_list.append([[row["token"]], row["ID"]])

            # list for all NPs in the sentence
            all_nps_of_sentence = list()

            # go through the dataframe once again
            for index, row in df.iterrows():

                # if the wordtype is a noun
                if row["wordtype"] == "N":

                    # create list for the NP:
                    current_np_ids = list()

                    # get all the info of the noun
                    info_of_noun = df.loc[index, :].txt_id_dta.flatten().tolist()

                    id_of_noun = info_of_noun[0]
                    head_of_noun_ID = info_of_noun[6]

                    # get ID of head of noun (+ e.g. verb particle)
                    head_ids = []
                    if head_of_noun_ID != 0:
                        head_ids.append(head_of_noun_ID)

                    # also store verb particle
                    for index2, row2 in df.iterrows():
                        if row2["head"] in head_ids and row2["wordtype"] == "PTKVZ":
                            head_ids.append(row2["ID"])

                    # get head of the head as well
                    super_head_ids = []

                    if int(head_of_noun_ID) > 0:
                        super_head_ID = df.loc[int(head_of_noun_ID) - 1, "head"]
                        super_head_ids.append(super_head_ID)

                        # also store verb particle
                        for index2, row2 in df.iterrows():
                            if (
                                row2["head"] in super_head_ids
                                and row2["wordtype"] == "PTKVZ"
                            ):
                                super_head_ids.append(row2["ID"])

                    # append the nouns ID to the list
                    current_np_ids.append(id_of_noun)

                    # in the following:
                    # check if any word refers to the noun as head
                    for ind, token_head_pair in enumerate(token_head_list):

                        # check if the ID of the noun is the deprel of
                        # another token --> noun is head of that token
                        if id_of_noun == token_head_pair[1]:

                            candidate_id = token_id_list[ind][1]

                            # append the ID of the token of the sentence
                            # --> get a list with IDs, can sort them and
                            # then create a second list with the filled in token
                            # (information)

                            current_np_ids.append(candidate_id)

                            # if there is an adjective: append what belongs to the
                            # adjective as well
                            # (adverbs or coordinated adjectives)
                            # and everything that is dependent of that...
                            # so go through dataframe once top to bottom
                            # and once bottom to top
                            if df.loc[int(candidate_id) - 1, "wordtype"] == "ADJA":
                                adj_ids = [candidate_id]
                                for index2, row2 in df.iterrows():
                                    if (
                                        row2["head"] in adj_ids
                                        and not row2["ID"] in current_np_ids
                                    ):
                                        current_np_ids.append(row2["ID"])
                                        adj_ids.append(row2["ID"])

                                for index2, row2 in df[::-1].iterrows():
                                    if (
                                        row2["head"] in adj_ids
                                        and not row2["ID"] in current_np_ids
                                    ):
                                        current_np_ids.append(row2["ID"])
                                        adj_ids.append(row2["ID"])

                            # if there is a verb (postnominal modifier e.g.
                            # object clause or relative clause)
                            # append verb particle as well
                            if df.loc[int(candidate_id) - 1, "wordtype"] == "V":
                                for index2, row2 in df.iterrows():
                                    if (
                                        row2["head"] == candidate_id
                                        and row2["wordtype"] == "PTKVZ"
                                    ):
                                        current_np_ids.append(row2["ID"])

                    current_np_ids.sort(key=int)
                    number_of_tokens_of_np = len(current_np_ids)

                    # create NP with the regarding token information, based on the IDs
                    current_np = list()

                    for token_id in current_np_ids:
                        index_in_df = int(token_id) - 1
                        if int(index_in_df) < 0:
                            token_info = tuple(
                                df.loc[int(token_id), :].txt_id_dta.flatten().tolist()
                            )
                        else:
                            token_info = tuple(
                                df.loc[int(index_in_df), :]
                                .txt_id_dta.flatten()
                                .tolist()
                            )

                        current_np.append(token_info)

                    # extract info of the head of the noun including verb particle
                    head_info = []

                    for head_id in sorted(head_ids, key=int):
                        if int(head_of_noun_ID) > 0:
                            info = (
                                df.loc[int(head_id) - 1, :]
                                .txt_id_dta.flatten()
                                .tolist()
                            )
                            head_info.append(info)

                    # if present, extract info of the super head, e.g. head of
                    # preposition ("liegt unter"...)
                    # including verb particles
                    super_head_info = []
                    for super_head_id in sorted(super_head_ids, key=int):
                        if int(super_head_id) > 0:
                            info = (
                                df.loc[int(super_head_id) - 1, :]
                                .txt_id_dta.flatten()
                                .tolist()
                            )
                            super_head_info.append(info)

                    """
                    create the final form of the single np on form of:
                    [	Sentence_NP_ID,
                        Filename of the input file {str},
                        Whole Sentence {str}, 
                        [head info] {list},
                        [super head info] {list},
                        number-of-tokens-in-NP {int},
                        [NP] {list}, e.g..: [(token1, POS-tag, grammatical_info,...),
                        ... (token-n, POS-tag, grammatical_info,...)],
                    ]
                    """

                    sentence_np_id = str(sentence_counter) + "_" + str(np_counter)
                    infilename = infile

                    final_form_of_np = [
                        sentence_np_id,
                        infilename,
                        sentence_as_string,
                        super_head_info,
                        head_info,
                        number_of_tokens_of_np,
                        current_np,
                    ]

                    np_counter += 1

                    all_nps_of_sentence.append(final_form_of_np)

            # --> clear the list of the single sentence for the new sentence
            single_sentence = list()

            sentence_counter += 1

            if len(all_nps_of_sentence) > 0:  # ignore empty lines
                nps_of_file.append(all_nps_of_sentence)

    # print the final list into a file that can be read in as a literal Python list
    # for the other groups to process further
    with open(outfile, "w", encoding="UTF-8-sig") as f:
        # pprint.pprint(nps_of_file)
        pprint.pprint(nps_of_file, f)


#########################
# main
#########################

if __name__ == "__main__":
    pass
