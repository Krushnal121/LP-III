public class Exp_1_FibonacciSeries {
    public static int recursive(int n) {
        if (n<=1) {return n;}
        return recursive(n-1)+recursive(n-2);
        //Time Complexity: O(2^n)
        //Space Complexity: O(n)
    }

    public static int iterative(int n) {
        int prev = 0;
        int cur = 1;
        int next = 0;
        for (int i = 2; i <= n; i++) {
            next = prev + cur;
            prev = cur;
            cur = next;
        }
        return cur;
        //Time Complexity: O(n)
        //Space Complexity: O(1)
    }

    public static void main(String[] args) {
        System.out.println(recursive(10));
        System.out.println(iterative(10));
    }
}
