//----------------------------------------------------------------------------------//
//Project: ListNet																	//
//Author: Ngo Xuan Bach, School of Information Science, JAIST						//
//email: bachnx@jaist.ac.jp															//
//Date: April, 2010																	//
//Source Paper: Learning to Rank: From Pairwise Approach to Listwise Approach		//
//				ICML - 2007															//
//----------------------------------------------------------------------------------//

//The implementation file of Pair class
#include <fstream>
#include <map>
#include "Pair.h"

using namespace std;

//constructor
Pair::Pair(std::map<int,double> & _features, double _score){
	this->features = _features;
	this->score = _score;
}

//returns feature vector
map<int,double> Pair::getFeature() const{
	return this->features;
}

//returns value of a feature
double Pair::getFeatureValue( int index) const{
	map<int,double>::const_iterator iter;
	iter = this->features.find( index);
	if( iter == this->features.end())
		return 0;
	else
		return (*iter).second;
}

//returns the score
double Pair::getScore() const{
	return this->score;
}

//only for testing
void Pair::write(std::ofstream &out) const{
	out<<this->score;
	map<int,double>::const_iterator iter;
	for(iter = this->features.begin(); iter != this->features.end(); iter++){
		out<<" "<<(*iter).first<<":"<<(*iter).second;
	}
	out<<endl;
}