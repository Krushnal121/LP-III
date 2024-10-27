import java.util.Comparator;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Scanner;

class DAA_2_HuffmanEncoding {
    public static void printCode(HuffmanNode root, String s) {
        if (root.left == null && root.right == null
                && Character.isLetter(root.c)) {
            System.out.println(root.c + ":" + s);
            return;
        } else {
            printCode(root.left, s + "0");
            printCode(root.right, s + "1");
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the string to convert into Huffman Code");
        String s = sc.nextLine();
        HashMap<Character, Integer> hm = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            hm.put(s.charAt(i), hm.getOrDefault(s.charAt(i), 0) + 1);
        }
        Character[] charArray = hm.keySet().toArray(new Character[0]);
        PriorityQueue<HuffmanNode> q = new PriorityQueue<>(charArray.length, new MyComparator());
        for (Character character : charArray) {
            HuffmanNode hn = new HuffmanNode();
            hn.c = character;
            hn.data = hm.get(character);
            hn.left = null;
            hn.right = null;
            q.add(hn);
        }
        HuffmanNode root = null;
        while (q.size() > 1) {
            HuffmanNode x = q.peek();
            q.poll();
            HuffmanNode y = q.peek();
            q.poll();
            HuffmanNode f = new HuffmanNode();
            f.data = x.data + y.data;
            f.c = '-';
            f.left = x;
            f.right = y;
            root = f;
            q.add(f);
        }
        printCode(root, "");
    }
}

class HuffmanNode {
    int data;
    char c;
    HuffmanNode left;
    HuffmanNode right;
}

class MyComparator implements Comparator<HuffmanNode> {
    public int compare(HuffmanNode x, HuffmanNode y) {
        return x.data - y.data;
    }
}