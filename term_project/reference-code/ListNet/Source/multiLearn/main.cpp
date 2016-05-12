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
#include <windows.h>
#include <vector>
#include <map>
#include <string>
#include <math.h>
#include "lib.h"
#include "Pair.h"
#include "Sample.h"

using namespace std;

//max number of features
int max_index = 1000;

//------------------------------Function Declaration--------------------------------//
//initialize parameters
vector<double> init();

//get pair from a line
Pair getPair( string line);

//reads samples from data file
vector<Sample> readSamples(const char* data_file);

//trains
void train(vector<Sample> & samples, int iteration, double learning_rate, vector<double> & params);

//input is a directory containing files
vector<double> multiLearn( const char* dir_path, int iteration, double learning_rate);

//write parameters to file
void writeParams( vector<double> & params, const char * model_file);
//----------------------------------------------------------------------------------//

//---------------------------------Main---------------------------------------------//
int main( int argc, char* argv[]){
	//checks arguments
	if( argc != 5){
		cout<<"------------------------------------------------------------------"<<endl;
		cout<<"ListNet - A listwise approach to learning-to-rank"<<endl;
		cout<<"Author: Ngo Xuan Bach, School of Information Science, JAIST"<<endl;
		cout<<"Source Paper (ICML 2007):"<<endl;
		cout<<"Learning to Rank: From Pairwise Approach to Listwise Approach"<<endl;
		cout<<"------------------------------------------------------------------"<<endl;
		cout<<"Usage: "<<argv[0]<<" dir_path iteration learning_rate model_file"<<endl;
		return -1;
	}

	//multi learn
	vector<double> params = multiLearn( argv[1], atoi(argv[2]), atof(argv[3]));

	//writes parameters to file
	writeParams( params, argv[4]);

	return 0;
}
//----------------------------------------------------------------------------------//

//------------------------------Function Definition---------------------------------//
//initialize parameters
vector<double> init(){
	vector<double> p;
	for( int i = 0; i < max_index; i++)
		p.push_back(0.0);	

	return p;
}

//get pair from a line
Pair getPair( string line){
	vector<string> items = Tokenize( line, " ");
	double score = atof( items[0].c_str());			//score
	
	map<int,double> features;
	for( unsigned int i = 2; i < items.size(); i++){
		vector<string> tmps = Tokenize( items[i], ":");
		int index = atoi( tmps[0].c_str());			//index of feature
		double value = atof( tmps[1].c_str());		//value of feature
		features.insert( make_pair( index, value));	//add feature	
	}

	return Pair( features, score);
}

//reads samples from file
vector<Sample> readSamples(const char* data_file){
	vector<Sample> samples;
	//opens data file to read
	ifstream in(data_file);

	string line;
	int cur_qid;	//current query id
	int pre_qid;	//previous query id

	getline( in, line);

	vector<Pair> pairs;
	bool start = true;
	while( !line.empty()){
		vector<string> items = Tokenize( line, " ");
		cur_qid = atoi( items[1].substr(4).c_str());

		if( start == true){
			pre_qid = cur_qid;
			start = false;
		}
		
		if( cur_qid == pre_qid){
			//continue a sample
			pairs.push_back( getPair( line));
		}else{
			//end of a sample
			samples.push_back( Sample(pairs));	//creates a new sample and adds to sample list
			pairs.clear();
			pairs.push_back( getPair( line));
			pre_qid = cur_qid;
		}

		//shifts line
		line.clear();
		getline( in, line);
	}

	//final sample
	samples.push_back( Sample( pairs));

	//closes data file
	in.close();

	return samples;	
}

//trains
void train(vector<Sample> & samples, int iteration, double learning_rate, vector<double> & params){
	//learns
	for( int i = 0; i < iteration; i++){
		for( unsigned int j = 0; j < samples.size(); j++){
			vector<Pair> pairs = samples[j].getData();
			int num_of_pairs = pairs.size();

			//calculate total exp of score
			double total_exp_of_score = 0;
			for( int t = 0; t < num_of_pairs; t++){
				total_exp_of_score += exp( pairs[t].getScore()); 
			}

			//calculates dot product
			vector<double> dotProducts;
			for( int t = 0; t < num_of_pairs; t++){
				//dot product
				double product = 0;
				map<int,double>::const_iterator iter;				
				map<int,double> features = pairs[t].getFeature();
				for( iter = features.begin(); iter != features.end(); iter++){
					product += params[iter->first-1] * iter->second;
				}			

				dotProducts.push_back(product);
			}

			//calculate total exp of predicted score
			double total_exp_of_predicted_score = 0;
			for( int t = 0; t < num_of_pairs; t++){
				total_exp_of_predicted_score += exp( dotProducts[t]);
			}

			//update params
			for( int k = 0; k < max_index; k++){
				double delta_param = 0;
				for( int t = 0; t < num_of_pairs; t++){
					if( pairs[t].getFeatureValue(k+1) != 0){
						delta_param -= (exp( pairs[t].getScore())/total_exp_of_score)*pairs[t].getFeatureValue(k+1);					
						delta_param +=  (1/total_exp_of_predicted_score)*exp( dotProducts[t])*pairs[t].getFeatureValue(k+1);
					}
				}

				//update
				params[k] -= learning_rate * delta_param;
			}			
		}
	}
}


//input is a directory containing files
vector<double> multiLearn( const char* dir_path, int iteration, double learning_rate){
	//initialize parameters
	vector<double> params = init();

	//multi learn
	for( int i = 0; i < iteration; i++){
		cout<<"iteration :"<<i<<endl;
		string dirScan(dir_path);
		dirScan.append("\\*.*");
		
		WIN32_FIND_DATA info;
		HANDLE h = FindFirstFile( dirScan.c_str(), &info);
		if( h == INVALID_HANDLE_VALUE){
			return params;
		}
		
		do{
			if( (info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0)
				continue;	//skip directories
			//get file name
			string file_name( dir_path);
			file_name.append("\\");
			file_name.append( info.cFileName);

			cout<<"Processing file "<<file_name<<"..."<<endl;
			
			//reads samples
			vector<Sample> samples = readSamples( file_name.c_str());

			//train
			train( samples, 1, learning_rate, params);
		}while( FindNextFile(h, &info));

		FindClose( h); //closes scan dir
	}

	return params;
}

//write parameters to file
void writeParams( vector<double> & params, const char * model_file){
	//opens file to write
	ofstream out(model_file);

	//writes
	for( unsigned int i = 0; i < params.size(); i++){
		out<<params[i]<<endl;
	}

	//closes file
	out.close();
}

//----------------------------------------------------------------------------------//
