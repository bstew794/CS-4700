import java.util.Random;

public class BST{
    BSTNode root;

    public BST(){
        this.root = null;
    }

    void insert(int key){
        this.root =  insertRecur(this.root, key);
    }

    BSTNode insertRecur(BSTNode myRoot, int key){
        if (myRoot == null){
            myRoot = new BSTNode(key);
            return myRoot;
        }
        if (key < myRoot.key){
            myRoot.left = insertRecur(myRoot.left, key);
        }
        else if (key > myRoot.key){
            myRoot.right = insertRecur(myRoot.right, key);
        }
        return myRoot;
    }

    void displayInOrder(){
        displayRecur(this.root);
    }

    void displayRecur(BSTNode myRoot){
        if (myRoot != null){
            displayRecur(myRoot.left);
            System.out.println(myRoot.key);
            displayRecur(myRoot.right);
        }
    }

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        BST tree = new BST();
        Random random = new Random();

        for (int i = 0; i < 10; i++){
            int ranInt = random.nextInt(1000);

            tree.insert(ranInt);
        }

        tree.displayInOrder();
        long endTime = System.currentTimeMillis();

        System.out.println("Program took " + (endTime - startTime) + " ms...");
    }

}
class BSTNode{
    int key;
    BSTNode left;
    BSTNode right;

    public BSTNode(int number) {
        this.key = number;
        this.left = this.right = null;
    }
}