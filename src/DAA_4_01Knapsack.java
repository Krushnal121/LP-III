import java.util.Scanner;

public class DAA_4_01Knapsack {

    // Function to solve 0/1 Knapsack problem using Dynamic Programming
    public static int knapSack(int W, int wt[], int val[], int n) {
        int[][] dp = new int[n + 1][W + 1];

        // Build the DP table in bottom-up manner
        for (int i = 0; i <= n; i++) {
            for (int w = 0; w <= W; w++) {
                if (i == 0 || w == 0) {
                    dp[i][w] = 0;
                } else if (wt[i - 1] <= w) {
                    dp[i][w] = Math.max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // The maximum profit for given capacity and items is in dp[n][W]
        return dp[n][W];
    }

    // Main method to test the knapSack function
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of items:");
        int n = sc.nextInt();

        int[] profit = new int[n];
        int[] weight = new int[n];

        System.out.println("Enter the profit and weight of each item:");
        for (int i = 0; i < n; i++) {
            System.out.print("Profit for item " + (i + 1) + ": ");
            profit[i] = sc.nextInt();
            System.out.print("Weight for item " + (i + 1) + ": ");
            weight[i] = sc.nextInt();
        }

        System.out.println("Enter the capacity of the knapsack:");
        int W = sc.nextInt();

        int maxProfit = knapSack(W, weight, profit, n);
        System.out.println("The maximum profit is: " + maxProfit);
    }
}