import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class Transposition {
    public static void railFence(String cisto) {
		int dolzinaBesedila=cisto.length();
        int kljuc=ThreadLocalRandom.current().nextInt(2, dolzinaBesedila/2);         //visina naj bo maksimalno polovica dolzine besedila
        System.out.println(kljuc);
        char [][] tab= new char [kljuc][cisto.length()];
        int vis=0;
        int sir=0;
		int gorDol=0;
        for(int i=0; i<cisto.length(); i++) {			//vpisemo v tabelo
            tab[vis][sir]=cisto.charAt(i);
            sir++;
            //if(vis+1==kljuc) {
            if(gorDol==0) {			//gremo dol
				if(vis+1==kljuc) {		//smo na podnu
					vis--;
					gorDol=1;
				}
				else {
					vis++;
				}
			}
			else if (gorDol==1) {
				if(vis-1==-1) {		//smo na vrhu
					vis++;
					gorDol=0;
				}
				else {
					vis--;
				}
			}
        }
		for(int i=0; i<kljuc; i++) {
			for(int j=0; j<cisto.length(); j++) {
				if(tab[i][j]=='\u0000') {
					System.out.print("- ");
				}
				else {
					System.out.print(tab[i][j]+" ");
				}
				if(j==cisto.length()-1) {
					System.out.println();
				}
			}
		}
		System.out.println();
        String tajnopis="";
		vis=0;
		sir=0;
		for(int i=0; i<cisto.length(); i+=0) {
			if(tab[vis][sir]=='\u0000') {
				if(sir+1==cisto.length()) {
					sir=0;
					vis++;
				}
				else {
					sir++;
				}
				continue;
            }
			tajnopis=tajnopis+tab[vis][sir];
			i++;
			if(tajnopis.length()==cisto.length()) {
				break;
			}
			if(sir+1==cisto.length()) {
                sir=0;
				vis++;
            }
            else {
                sir++;
            }
		}
        System.out.print(kljuc + " " + tajnopis);
    }
    
    public static void main (String [] args) {
        Scanner sc= new Scanner (System.in);
        String besedilo=sc.nextLine();
        String cistopis=besedilo.replaceAll("\\s","");
        //cistopis=cistopis.replaceAll("","");                                        //odstrani locila
        cistopis=cistopis.toUpperCase();
		System.out.println(cistopis);
        int sifriranje=ThreadLocalRandom.current().nextInt(1, 5);
        
        railFence(cistopis);
        /*if(sifriranje==1) {
            railFence(cistopis);
        }
        .
        .
        .
        }*/
    }
}