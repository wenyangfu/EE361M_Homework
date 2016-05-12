//----------------------------------------------------------------------------------//
//Project: ListNet																	//
//Author: Ngo Xuan Bach, School of Information Science, JAIST						//
//email: bachnx@jaist.ac.jp															//
//Date: April, 2010																	//
//Source Paper: Learning to Rank: From Pairwise Approach to Listwise Approach		//
//				ICML - 2007															//
//----------------------------------------------------------------------------------//

//The header file for Pair class

#ifndef _PAIR_H_
#define _PAIR_H_

#include <fstream>
#include <map>

using namespace std;

//the class of pair of a query and a document
class Pair{
	private:
		map<int,double> features;	//feature vector of the pair
		double score;				//score of the pair
	public:
		Pair( map<int,double> & _features, double _score);//constructor
		map<int,double> getFeature() const;				//returns feature vector
		double getFeatureValue( int index) const;		//returns value of a feature
		double getScore() const;						//returns the score

		void write(ofstream & out) const;		//only for testing
};

#endif
