import java.util.Scanner;

public class DAA_5_NQueens {
    private int n;
    private int[][] board;

    public DAA_5_NQueens(int n) {
        this.n = n;
        board = new int[n][n];
    }

    // Function to check if placing queen at board[row][col] is safe
    private boolean isSafe(int row, int col) {
        // Check this row on the left side
        for (int i = 0; i < col; i++) {
            if (board[row][i] == 1) {
                return false;
            }
        }

        // Check upper diagonal on the left side
        for (int i = row, j = col; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 1) {
                return false;
            }
        }

        // Check lower diagonal on the left side
        for (int i = row, j = col; j >= 0 && i < n; i++, j--) {
            if (board[i][j] == 1) {
                return false;
            }
        }

        return true;
    }

    // Recursive utility function to solve N-Queens problem
    private boolean solveNQueens(int col) {
        // Base case: If all queens are placed
        if (col >= n) {
            return true;
        }

        // Try placing a queen in each row for this column
        for (int i = 0; i < n; i++) {
            // Check if queen can be placed on board[i][col]
            if (isSafe(i, col)) {
                // Place this queen in board[i][col]
                board[i][col] = 1;

                // Recur to place the rest of the queens
                if (solveNQueens(col + 1)) {
                    return true;
                }

                // Backtrack if placing queen here doesn't lead to a solution
                board[i][col] = 0;
            }
        }

        // If no placement is possible, return false
        return false;
    }

    // Function to place the first queen and solve for remaining queens
    public boolean placeQueens() {
        // Place the first queen at board[0][0] (can be modified as needed)
        Scanner scanner = new Scanner(System.in);
        System.out.println("Where Would You Like To place Your First Queen in First Column?");
        board[scanner.nextInt()][0] = 1;

        // Solve for the remaining queens starting from column 1
        return solveNQueens(1);
    }

    // Function to print the n-Queens matrix
    public void printBoard() {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter The Size of Board");
        int n = scanner.nextInt(); // You can set n to any desired size
        DAA_5_NQueens nQueens = new DAA_5_NQueens(n);

        // Start placing queens and print the solution if it exists
        if (nQueens.placeQueens()) {
            System.out.println("Solution found:");
            nQueens.printBoard();
        } else {
            System.out.println("No solution exists for " + n + " queens.");
        }
    }
}
