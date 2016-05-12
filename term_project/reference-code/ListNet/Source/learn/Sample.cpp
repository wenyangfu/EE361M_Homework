//----------------------------------------------------------------------------------//
//Project: ListNet																	//
//Author: Ngo Xuan Bach, School of Information Science, JAIST						//
//email: bachnx@jaist.ac.jp															//
//Date: April, 2010																	//
//Source Paper: Learning to Rank: From Pairwise Approach to Listwise Approach		//
//				ICML - 2007															//
//----------------------------------------------------------------------------------//

//The implementation file for Sample class
#include <fstream>
#include <map>
#include <vector>
#include "Pair.h"
#include "Sample.h"

using namespace std;

//constructor
Sample::Sample( vector<Pair> & _data){
	this->data = _data;
}

//get data
vector<Pair> Sample::getData() const{
	return this->data;
}

//only for testing
void Sample::write(std::ofstream & out) const{
	for( unsigned int i = 0; i < this->data.size(); i++){
		this->data[i].write( out);
	}
}