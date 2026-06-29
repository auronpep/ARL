from arl.conlaw_import import infer_strategy_fields, row_to_question


def test_row_to_question_preserves_private_workbook_fields():
    row = {
        "Question Number": 7,
        "Question": "Congress conditions federal funds for universities.",
        "Answer Choice A": "Federal police power.",
        "Answer Choice B": "Spending power.",
        "Answer Choice C": "Article IV Privileges and Immunities.",
        "Answer Choice D": "Contracts Clause.",
        "Correct Answer": "B",
        "Answer Explanation": "Congress can spend for the general welfare.",
        "Wrong Answer Explanation": "A is wrong because there is no federal police power.",
    }

    question = row_to_question(row)

    assert question["id"] == "CONLAW-SET1-007"
    assert question["answer"] == "B"
    assert question["choices"]["A"] == "Federal police power."
    assert question["source"]["question_number"] == 7
    assert "private_notes" in question


def test_infer_strategy_fields_tags_federal_police_power_trap():
    text = "Congress conditions federal funds. A is wrong because there is no federal police power."

    inferred = infer_strategy_fields(text)

    assert inferred["dominant_trap_mechanic"] == "federal_police_power_bait"
    assert "CONLAW-FEDERAL-POLICE-POWER-BAIT-01" in inferred["expected_mechanic_ids"]
    assert "CONLAW-SPENDING-POWER-01" in inferred["expected_mechanic_ids"]
