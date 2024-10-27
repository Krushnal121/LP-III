import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Scanner;

class WeightNode {
    int weight;
    int profit;

    public WeightNode(int weight, int profit) {
        this.weight = weight;
        this.profit = profit;
    }
}

class DAA_3_FractionalKnapsack {


    public static double profitMaximizer(PriorityQueue<WeightNode> pq, int capacity) {
        int profit = 0;
        while (!pq.isEmpty() && capacity > 0) {
            WeightNode w = pq.poll();
            if (capacity > w.weight) {
                capacity -= w.weight;
                profit += w.profit;
            }
            else {
                int num=(w.profit*capacity)/w.weight;
                profit += w.profit*(capacity/w.weight);
            }
        }
        return profit;
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of items");
        int n = sc.nextInt();
        System.out.println("Enter the weight and profit seperated by space");
        PriorityQueue<WeightNode> pq = new PriorityQueue<>((WeightNode x, WeightNode y) -> {
            double X = (double) x.profit / x.weight;
            double Y = (double) y.profit / y.weight;
            return X < Y ? 1 : -1;
        });
        for (int i = 0; i < n; i++) {
            pq.add(new WeightNode(sc.nextInt(), sc.nextInt()));
        }
        System.out.println("Enter The Capacity of Knapsack");
        int capacity = sc.nextInt();
        System.out.println(profitMaximizer(pq, capacity));
    }
}