
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Testaccuracy {

	public static int Totalentity;
	public static int Nameentity;
	public static int Ontargetentity=0;
	public static int OntargetNentity=0;
	//public static Map<Integer,Integer> docRelation = new HashMap<Integer,Integer>();
	public static Map<Integer,List<Tag>> standardAns = Collections.synchronizedMap(new HashMap<Integer,List<Tag>>());
	public static Map<String,List<String>> redRelation = new HashMap<String,List<String>>();
	public static List<Tag> tagList=new ArrayList<Tag>();
	public static List<Tag> anList=new ArrayList<Tag>();
	//public static List<List<Tag>> bList=new ArrayList<List<Tag>>();
	
	static class Tag{
		int docnum;
		int offset;
		String type;
		String entity;
		String mention;
	}
	
	public static String filterStr(String str){
		if(str.toLowerCase().startsWith("en:")&&str.length()>3)
			str=str.substring(3,str.length());
		if(str.toLowerCase().startsWith("the ")&&str.length()>4)
			str=str.substring(4,str.length());
		else if(str.toLowerCase().startsWith("a ")&&str.length()>2)
			str=str.substring(2,str.length());
		if(str.endsWith("'s")&&str.length()>2)
			str=str.substring(0,str.length()-2);
		return str;
	}
	public static boolean judgeEqualm(String str1,String str2){
		str1=filterStr(str1);
		str2=filterStr(str2);
		if(str1.replace(" ", "").equalsIgnoreCase(str2.replace(" ", "")))
			return true;
		else
			return false;
	}
	public static boolean judgeEquale(String str1,String str2){
		str1=filterStr(str1.replace("_", " "));
		str2=filterStr(str2.replace("_", " "));
		if(str1.replace(" ", "").equalsIgnoreCase(str2.replace(" ", "")))
			return true;
		else 
			return false;
	}
	public static String[] parseStr(String str){
		String[] strs = new String[4];
		strs[0]=str.substring(0,str.indexOf(" "));
		str=str.substring(str.indexOf(" ")+1,str.length());
		strs[1]=str.substring(0,str.indexOf(" "));
		str=str.substring(str.indexOf(" ")+1,str.length());
		strs[2]=str.substring(0,str.indexOf(" "));
		strs[3]=str.substring(str.indexOf(" ")+1,str.length());
		return strs;
	}
	/*public static void getdocRelation(){
		String path="";
		File file=new File(path);
		FileReader fr;
		String str;
		try{
			fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			while((str=br.readLine())!=null){
				String[] lstr=str.split("	");
				docRelation.put(Integer.parseInt(lstr[1].substring(0,lstr[1].indexOf(".txt"))), Integer.parseInt(lstr[0]));
				if(Integer.parseInt(lstr[0])==1500)
					break;
			}
			br.close();
			fr.close();
		}catch (Exception e){
			e.printStackTrace();
		}
	}*/
	public static void getStandans(){
		String path="standard_result.txt";
		Totalentity=0;
		Nameentity=0;
		String str;
		int rem=-1;
		int total=0;
		File file=new File(path);
		FileReader fr;
		try {
			fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			while((str=br.readLine())!=null){
				String[] st=str.split("	");
				if(st[0].contains("result"))
					st[0]=st[0].substring(0,st[0].indexOf("r"));
				if(st.length!=5)
					continue;
				else{
					if((rem!=-1)&&(rem!=Integer.parseInt(st[0]))){
						List<Tag> aList=new ArrayList<Tag>();
						for(int i=0;i<anList.size();i++)
							aList.add(anList.get(i));
						standardAns.put(rem, aList);
						anList.clear();
						total++;
						rem=-1;
					}
					Tag tag=new Tag();
					tag.docnum=Integer.parseInt(st[0]);
					tag.offset=Integer.parseInt(st[1]);
					tag.type=st[4];
					tag.entity=st[2];
					tag.mention=st[3];
					Totalentity++;
					if(tag.type.equals("2"))
						Nameentity++;
					anList.add(tag);
					rem=tag.docnum;
				}
			}
			total++;
			List<Tag> aList=new ArrayList<Tag>();
			for(int i=0;i<anList.size();i++)
				aList.add(anList.get(i));
			standardAns.put(rem, aList);
			anList.clear();
			br.close();
			fr.close();
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public static void getRedirect(){
		String path="redirect.txt";
		String str;
		File file=new File(path);
		FileReader fr;
		try {
			fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			while((str=br.readLine())!=null){
				String[] st=str.split("	");
				if(st.length>1){
					List<String> strList = new ArrayList<String>();
					for(int i=1;i<st.length;i++)
						strList.add(st[i]);
					redRelation.put(st[0], strList);
				}
				}
			br.close();
			fr.close();
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public static void judgeCurracy(int rem){
		int docnum=rem;
		List<Tag> ansList=new ArrayList<Tag>();
		//if(docRelation.get(rem)==null)
			//return;
		//rem=docRelation.get(rem);
		ansList=standardAns.get(rem);
		if(ansList==null)
			return;
		for(int i=0;i<ansList.size();i++){
			String entityname = "";
			for(int j=0;j<tagList.size();j++){
				if((tagList.get(j).offset-21<ansList.get(i).offset)&&(tagList.get(j).offset+21>ansList.get(i).offset))
					if(judgeEqualm(tagList.get(j).mention,ansList.get(i).mention)){
						if(ansList.get(i).entity.endsWith("_"))
							entityname=ansList.get(i).entity.substring(0,ansList.get(i).entity.length()-1);
						else
							entityname=ansList.get(i).entity;
						if(entityname.contains("'"))
							entityname=entityname.replace("'", "\\'");
						if(judgeEquale(tagList.get(j).entity,entityname)){
							Ontargetentity++;
							if(ansList.get(i).type.equals("2"))
								OntargetNentity++;
						}
						else{
							List<String> strList = new ArrayList<String>();
							strList=redRelation.get(ansList.get(i).entity);
							if(strList!=null)
								for(int k=0;k<strList.size();k++)
									if(judgeEquale(strList.get(k),tagList.get(j).entity)){
										Ontargetentity++;
										if(ansList.get(i).type.equals("2"))
											OntargetNentity++;
										break;
									}
						}
					}
				}
			}
	}
	@SuppressWarnings("unchecked")
	public static void main(String[] args){
		String path="answer.txt";
		//getdocRelation();
		getStandans();
		getRedirect();
		String str;
		int rem=-1;
		int total=0;
		int totalTag=0;
		File file=new File(path);
		FileReader fr;
		try {
			fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			while((str=br.readLine())!=null){
				String[] st=str.split("	");
				if(st[0].contains("result"))
					st[0]=st[0].substring(0,st[0].indexOf("r"));
				if(st.length!=4)//||docRelation.get(Integer.parseInt(st[0]))==null)
					continue;
				else{
					totalTag++;
					if((rem!=-1)&&(rem!=Integer.parseInt(st[0]))){
						judgeCurracy(rem);
						tagList.clear();
						total++;
						rem=-1;
					}
					Tag tag=new Tag();
					tag.docnum=Integer.parseInt(st[0]);
					tag.offset=Integer.parseInt(st[1]);
					tag.entity=st[2];
					tag.mention=st[3];
					tag.type="";
					tagList.add(tag);
					rem=tag.docnum;
				}
			}
			total++;
			judgeCurracy(rem);
			br.close();
			fr.close();
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Totalentity:"+Totalentity);
		System.out.println("Nameentity:"+Nameentity);
		System.out.println("Ontargetentity:"+Ontargetentity);
		System.out.println("OntargetNentity:"+OntargetNentity);
		System.out.println("totalTag:"+totalTag);
		System.out.println("Recall of PN + DC: "+(float)Ontargetentity/Totalentity);
		System.out.println("Recall of PN: "+(float)OntargetNentity/Nameentity);
		System.out.println("Prec. of PN + DC: "+(float)Ontargetentity/totalTag);
	}
}
