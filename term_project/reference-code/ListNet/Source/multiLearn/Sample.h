//----------------------------------------------------------------------------------//
//Project: ListNet																	//
//Author: Ngo Xuan Bach, School of Information Science, JAIST						//
//email: bachnx@jaist.ac.jp															//
//Date: April, 2010																	//
//Source Paper: Learning to Rank: From Pairwise Approach to Listwise Approach		//
//				ICML - 2007															//
//----------------------------------------------------------------------------------//

//The header file for Sample class
#ifndef _SAMPLE_H_
#define _SAMPLE_H_

#include <fstream>
#include <map>
#include <vector>
#include "Pair.h"

using namespace std;

class Sample{
	private:
		vector<Pair> data;	//vector of Pairs
	public:
		Sample( vector<Pair> & _data);	//constructor
		vector<Pair> getData() const;	//get data
		void write( ofstream & out) const;//only for testing
};

#endif