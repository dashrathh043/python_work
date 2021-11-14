def longestCommonSubsequence(s1, s2):
    row, col = (len(s1) + 1, len(s2) + 1)
    array = [[None] * col for i in range(row)]
    for i in range(0, len(s1) + 1):
        for j in range(0, len(s2) + 1):
            if i == 0 or j == 0:
                array[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                array[i][j] = array[i - 1][j - 1] + 1
            else:
                array[i][j] = max(array[i][j - 1], array[i - 1][j])
    print(array)
    return array[len(s1)][len(s2)]


def longestCommonSubstring(s1, s2):
    row, col = (len(s1) + 1, len(s2) + 1)
    table = [[None] * col for i in range(row)]
    maxsub = 0
    for i in range(0, len(s1) + 1):
        for j in range(0, len(s2) + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
                if table[i][j] > maxsub:
                    maxsub = table[i][j]
    print(table)
    return maxsub


def minCostConvertOneStringToSecondString(s1, s2):
    row, col = (len(s1) + 1, len(s2) + 1)
    table = [[0] * col for i in range(row)]
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            table[i][0] = table[i - 1][0] + 1
            table[0][j] = table[0][j - 1] + 1
            if s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = min(table[i][j - 1] + 1, table[i - 1][j] + 1, table[i - 1][j - 1] + 1)

    return table[len(s1)][len(s2)]


def findNumberOfSubset(input_list, sum):
    row, col = (len(input_list) + 1, sum + 1)
    table = [[0] * col for i in range(row)]

    print(row, col)

    for i in range(1, row + 1):
        table[i - 1][0] = 1
    for j in range(1, sum + 1):
        table[0][j] = 0

    for i in range(1, row):
        for j in range(1, col):
            if input_list[i - 1] > j:
                table[i][j] = table[i - 1][j]
            else:
                table[i][j] = table[i - 1][j] + table[i - 1][j - input_list[i - 1]]
    print(table)
    return table[row - 1][col - 1]


def coinChangeProblem(cointList, amount):
    table = [int(0) for i in range(amount + 1)]
    table[0] = 1

    for i in range(0, len(cointList)):
        j = cointList[i]
        while j < len(table):
            table[j] = table[j] + table[j - cointList[i]]
            j = j + 1
        print(table)
    return table[amount]


print(coinChangeProblem([1, 2, 5], 11))
