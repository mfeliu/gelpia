#include "optimizer_types.h"


using boost::numeric::interval;
using std::vector;
using std::function;



/*
 * Divides given interval box along longest dimension
 * Arguments:
 *          X - given box
 * Return: vector of two new boxes
 */
vector<box_t> split_box(const box_t & X)
{
  // Split the box along longest dimension
  double longest = 0.0;
  int longest_idx = 0;
  for(uint i = 0; i < X.size(); ++i) {
    if(width(X[i]) > longest) {
      longest = width(X[i]);
      longest_idx = i;
    }
  }

  // create two copies
  box_t X1(X);
  box_t X2(X);

  // split boxes along longest dimension
  double m = median(X[longest_idx]);
  X1[longest_idx].assign(X1[longest_idx].lower(), m);
  X2[longest_idx].assign(m, X2[longest_idx].upper());

  return vector<box_t>{X1, X2};
}


/*
 * Finds midpoint of given box
 * Arguments:
 *          X - given box
 * Return: box whose dimentions align to the single midpoint
 */
box_t midpoint(const box_t & X)
{
  box_t result(X.size());

  for(uint i = 0; i < X.size(); i++) {
    double m = median(X[i]);
    result[i].assign(m,m);
  }

  return result;
}


/*
 * Caluclates the width of the box, the length of the longest dimension
 * Arguments:
 *          X - given box
 * Return: width scalar
 */
double width(const box_t & X)
{
  double longest = 0.0;
  for(uint i = 0; i < X.size(); i++) {
    if(width(X[i]) > longest) {
      longest = width(X[i]);
    }
  }

  return longest;
}