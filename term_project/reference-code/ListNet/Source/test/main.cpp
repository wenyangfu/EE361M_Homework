//----------------------------------------------------------------------------------//
//Project: ListNet																	//
//Author: Ngo Xuan Bach, School of Information Science, JAIST						//
//email: bachnx@jaist.ac.jp															//
//Date: April, 2010																	//
//Source Paper: Learning to Rank: From Pairwise Approach to Listwise Approach		//
//				ICML - 2007															//
//----------------------------------------------------------------------------------//

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "lib.h"

using namespace std;

//------------------------Function Declaration---------------------------------------//
vector<double> readModel( const char * model_file);

void test( const char * model_file, const char * data_file, const char * output_file);
//-----------------------------------------------------------------------------------//

//-----------------------Main function-----------------------------------------------//
int main( int argc, char * argv[]){
	//checks arguments
	if( argc != 4){
		cout<<"------------------------------------------------------------------"<<endl;
		cout<<"ListNet - A listwise approach to learning-to-rank"<<endl;
		cout<<"Author: Ngo Xuan Bach, School of Information Science, JAIST"<<endl;
		cout<<"Source Paper (ICML 2007):"<<endl;
		cout<<"Learning to Rank: From Pairwise Approach to Listwise Approach"<<endl;
		cout<<"------------------------------------------------------------------"<<endl;
		cout<<"Usage: "<<argv[0]<<" model_file data_file output_file"<<endl;
		return -1;
	}

	//tests
	test(argv[1], argv[2], argv[3]);
	return 0;
}
//-----------------------------------------------------------------------------------//

//-------------------------Function Definition---------------------------------------//
vector<double> readModel( const char * model_file){
	vector<double> params;
	//opens file to read
	ifstream in( model_file);

	string line;
	getline( in, line);

	while( !line.empty()){
		params.push_back( atof(line.c_str()));

		//shifts line
		line.clear();
		getline( in, line);
	}

	//closes
	in.close();

	return params;
}

void test( const char * model_file, const char * data_file, const char * output_file){
	vector<double> params = readModel( model_file);

	//opens file to read and write
	ifstream in( data_file);
	ofstream out( output_file);

	string line;
	getline( in, line);

	while( !line.empty()){
		double score = 0;
		vector<string> items = Tokenize( line, " ");
		for( unsigned int i = 2; i < items.size(); i++){
			vector<string> tmps = Tokenize( items[i], ":");
			int index = atoi( tmps[0].c_str());
			double value = atof( tmps[1].c_str());

			if( index <= params.size())
				score += params[index-1] * value;
		}

		//out<<items[0]<<" "<<score<<endl;	
		out<<score<<endl;	
		
		//shift line
		line.clear();
		getline( in, line);
	}

	//closes
	in.close();
	out.close();
}
//-----------------------------------------------------------------------------------//