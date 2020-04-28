""""
Open your PyCharm Or IDLE or your favourite Code Editor. Create a function named func_single_multiplication.
It should take as input a parameter called number, then it should display the multiplication table (from 1 to 10) of
this number.
For the display - use any beautiful creative style you want.

Create another function called func_many_multiplication.
It should take as input a parameter called number and will display the multiplication table of each number from 1 to
that input parameter.
For instance, if input number is 4, then it should display the table of 1, 2, 3 and 4.

Please notice that the function called func_many_multiplication should use the first function called
func_single_multiplication.
"""


def func_single_multiplication(number: int) -> None:
    """
    Print a multiplication table (1 to 10) for a given number
    :param number: number for which to create a multiplication table
    :return: None
    """
    print(f'Multiplication table from 1 to 10 for {number}')

    # we want to make sure that the resuls are printed right justified; so we need to know the max length of the output
    result_length = len(str(10 * number))

    # iterate 1..10
    for i in range(1, 11):
        print(f'{i:2} x {number} = {number * i:{result_length}}')


def func_many_multiplication(number: int) -> None:
    """
    Display the multiplication table of each number from 1 to the given parameter
    :param number: Maximum number to display a multiplication table for
    :return: None
    """
    for i in range(1, number + 1):
        func_single_multiplication(i)
        print()


if __name__ == '__main__':
    func_many_multiplication(10)
