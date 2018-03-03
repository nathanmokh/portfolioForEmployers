package commandLine;

import java.util.*;

import com.sun.org.apache.xml.internal.dtm.ref.DTMDefaultBaseIterators.ChildrenIterator;
public class DirectoryTree {
	
	//keeps track of number of nodes for numNodes() method
	public int nodeTotal = 0;
	public String path = "";
	private class Node {
		String name;
		Node parent;
		LinkedList<Node> children = new LinkedList<Node>();
		Node (String name, Node parent) {
			this.name = name;
			this.parent = parent;
		}
		void addChild (Node child) {
			children.add(child);
		}
	}
	Node root = new Node ("", null);
	Node cur = root;
	public boolean mkdir (String name) {
		for (Node child : cur.children) {
			if (child.name.equals(name)) {
				return false;
			}
		}
		Node add = new Node(name, cur);
		cur.addChild(add);
		nodeTotal++;
		return true;
	}
	
	public boolean cd (String name) {
		//have a special case for no children
		if (name.equals("..")) {
			cdUp();
			
			return true;
		} 
		//call cdUp()
		for (Node child : cur.children) {
			if (child.name.equals(name)) {
				cur = child;
				path += "/" + child.name;
				return true;
			}
		}
		return false;
	}
	
	public boolean cdUp() {
		//Have a special case for root
		if (cur == root) {
			return false;
		}
		cur = cur.parent;
		//code below deletes the last element in the path string
		char[] pathArray = path.toCharArray();
		int lastSlashIndex = 0;
		int i = 0;
		for (char elements : pathArray) {
			if (elements == '/') {
				lastSlashIndex = i;
			}
			i++;
		}
		char [] arrayWithoutLastElement = Arrays.copyOfRange(pathArray, 0, lastSlashIndex);
		path =  new String(arrayWithoutLastElement);
		//end of deleting last element code
		return true;
	}
	
	public boolean rmdir (String name) {
		for (Node child : cur.children) {
			if (child.name.equals(name)) {
				cur.children.remove(child);
				nodeTotal--;
				return true;
			}
		}
		return false;
	}

	public String ls () {
		String ret = "";
		for (Node x : cur.children) {
			ret += x.name + "\n";
		}
		return ret;
	}
	public boolean hasChildren(Node n) {
		if (n.children == null) return false;
		else return true;
	}
	
	public int amountOfChildren(Node parent) {
		if (hasChildren(parent) == false) {
			return 0;
		} else {
			int i = 0;
			for (Node child : parent.children) {
				i++;
			}
			return i;
		}
	}
	

	private String printPreOrder(Node n, int depth) {
		String ret = "";
		if (depth != 0) {
			for (int i = 0; i<depth; i++) {
				ret+= "  ";
			}
		}
		ret+=n.name + "\n";
		for (Node child : n.children) {
			ret += printPreOrder(child, depth+1);
		}
		return ret;
	}


	public String printSubTree() {
		return printPreOrder(cur, 0);
	}
	
	public String pwd () {
		if (cur.name == "") {
			return "/";
		}
		return path;
	}
	
	public int numNodes() {
		//returns number of children + 1 in a directory
		int ret = 1;
		for (Node child : cur.children) {
			ret++;
		}
		return ret;
	}
}