
import java.util.Arrays;
import java.util.Comparator;

class Job {
    int id;       // Job ID
    int deadline; // Job deadline
    int profit;   // Job profit

    public Job(int id, int deadline, int profit) {
        this.id = id;
        this.deadline = deadline;
        this.profit = profit;
    }
}

public class JobSequence {

    // Function to find the maximum profit job sequence
    public static void jobSequencingWithDeadline(Job[] jobs, int n) {
        // Sort jobs in decreasing order of profit
        Arrays.sort(jobs, (a, b) -> b.profit - a.profit);

        // To keep track of free time slots
        boolean[] slots = new boolean[n];
        int[] result = new int[n]; // To store result sequence of job IDs

        // Initialize all slots to be free
        Arrays.fill(slots, false);

        int totalProfit = 0;

        // Iterate through all jobs
        for (Job job : jobs) {
            // Find a free slot for this job (start from the last possible slot)
            for (int j = Math.min(n, job.deadline) - 1; j >= 0; j--) {
                if (!slots[j]) { // If slot is free
                    result[j] = job.id; // Assign this job to the slot
                    slots[j] = true; // Mark this slot as occupied
                    totalProfit += job.profit; // Add profit
                    break;
                }
            }
        }

        // Print the sequence of jobs
        System.out.print("Job sequence for maximum profit: ");
        for (int i = 0; i < n; i++) {
            if (slots[i]) {
                System.out.print("Job" + result[i] + " ");
            }
        }
        System.out.println("\nTotal Profit: " + totalProfit);
    }

    public static void main(String[] args) {
        // Define jobs with {job_id, deadline, profit}
        Job[] jobs = {
                new Job(1, 2, 100),
                new Job(2, 1, 19),
                new Job(3, 2, 27),
                new Job(4, 1, 25),
                new Job(5, 3, 15)
        };

        int n = jobs.length;

        jobSequencingWithDeadline(jobs, n);
    }
}
