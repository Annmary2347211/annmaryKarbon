import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field


# This is already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index: int) -> float:
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for calculation.
    :return: The net revenue value from the financial data.
    """
    financials = data["financials"][financial_index]
    try:
        return financials["pnl"]["lineItems"]["net_revenue"]
    except KeyError:
        print("net_revenue key not found")
        return 0


def total_borrowing(data: dict, financial_index: int) -> float:
    """
    Calculate the total borrowings for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data.

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for calculation.
    :return: The total borrowings.
    """
    financials = data["financials"][financial_index]
    
    # Use .get() to safely access 'longTermBorrowing' and provide a default of 0 if it's missing
    long_term_borrowing = financials["bs"]["liabilities"].get("long_term_borrowings", 0)
    short_term_borrowing = financials["bs"]["liabilities"].get("short_term_borrowings", 0)

    total_borrowing = long_term_borrowing + short_term_borrowing
    return total_borrowing


def iscr(data: dict, financial_index: int) -> float:
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is calculated as (Profit Before Interest and Tax + Depreciation + 1) divided by (Interest expenses + 1).
    The addition of 1 is to avoid division by zero.

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for the ISCR calculation.
    :return: The ISCR value.
    """
    financials = data["financials"][financial_index]
    profit_before_interest_tax = financials["pnl"]["lineItems"]["profit_before_tax"]
    depreciation = financials["pnl"]["lineItems"].get("depreciation", 0)
    interest_expenses = financials["pnl"]["lineItems"].get("interest", 0)
    
    return (profit_before_interest_tax + depreciation + 1) / (interest_expenses + 1)


def iscr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    If ISCR >= 2, assign a GREEN flag; otherwise, assign a RED flag.

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for the ISCR calculation.
    :return: FLAGS.GREEN or FLAGS.RED based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    if iscr_value >= 2:
        return FLAGS.GREEN
    return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    If total revenue >= 50 million, assign a GREEN flag; otherwise, assign a RED flag.

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for the revenue calculation.
    :return: FLAGS.GREEN or FLAGS.RED based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    if revenue >= 50_000_000:
        return FLAGS.GREEN
    return FLAGS.RED


def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    If borrowing to revenue ratio <= 0.25, assign a GREEN flag; otherwise, assign an AMBER flag.
    If total revenue is 0, avoid division by zero and return a RED flag indicating risk.

    :param data: A dictionary containing financial data.
    :param financial_index: The index of the financial entry to be used for the ratio calculation.
    :return: FLAGS.GREEN or FLAGS.AMBER or FLAGS.RED based on the borrowing to revenue ratio.
    """
    total_borrowings_value = total_borrowing(data, financial_index)
    total_revenue_value = total_revenue(data, financial_index)

    if total_revenue_value == 0:
        print("Total revenue is zero, cannot calculate borrowing to revenue ratio.")
        return FLAGS.RED  # Return RED flag since no revenue means a higher risk.

    ratio = total_borrowings_value / total_revenue_value

    if ratio <= 0.25:
        return FLAGS.GREEN
    return FLAGS.AMBER

