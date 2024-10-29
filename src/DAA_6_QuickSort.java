import java.util.Arrays;
import java.util.Random;

public class DAA_6_QuickSort {
    // Function to perform Deterministic QuickSort
    public static void deterministicQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = deterministicPartition(arr, low, high);
            deterministicQuickSort(arr, low, pivotIndex - 1);
            deterministicQuickSort(arr, pivotIndex + 1, high);
        }
    }

    // Partition function for Deterministic QuickSort
    private static int deterministicPartition(int[] arr, int low, int high) {
        int pivot = arr[high]; // using the last element as pivot
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    // Function to perform Randomized QuickSort
    public static void randomizedQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = randomizedPartition(arr, low, high);
            randomizedQuickSort(arr, low, pivotIndex - 1);
            randomizedQuickSort(arr, pivotIndex + 1, high);
        }
    }

    // Partition function for Randomized QuickSort
    private static int randomizedPartition(int[] arr, int low, int high) {
        int randomPivotIndex = new Random().nextInt(high - low + 1) + low;
        swap(arr, randomPivotIndex, high); // Move random pivot to the end
        return deterministicPartition(arr, low, high); // Use the same deterministic partition
    }

    // Utility function to swap two elements in an array
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // Function to generate a random array of given size
    private static int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(10); // Random integers between 0 and 9999
        }
        return arr;
    }

    public static void main(String[] args) {
        int size = 10; // Size of the array for analysis
        int[] arr1 = generateRandomArray(size);
        int[] arr2 = Arrays.copyOf(arr1, arr1.length); // Copy of arr1 for comparison

        // Measure time for Deterministic QuickSort
        long startTime = System.nanoTime();
        deterministicQuickSort(arr1, 0, arr1.length - 1);
        long endTime = System.nanoTime();
        System.out.println("Time taken by Deterministic QuickSort: " + (endTime - startTime) / 1e6 + " ms");

        // Measure time for Randomized QuickSort
        startTime = System.nanoTime();
        randomizedQuickSort(arr2, 0, arr2.length - 1);
        endTime = System.nanoTime();
        System.out.println("Time taken by Randomized QuickSort: " + (endTime - startTime) / 1e6 + " ms");
    }
}
