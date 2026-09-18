#ifndef CCOMPLEX_H
#define CCOMPLEX_H

class CComplex
{
private:
    double mR;
    double mI;

public:
    CComplex(double zR = 0, double zI = 0);
    ~CComplex();
    void SetValue();
    void SetValue(double zR, double zI);
    void ShowValue();
    // 四则运算
    CComplex Add(const CComplex& zC) const;
    CComplex Substract(const CComplex& zC) const;
    CComplex Multiply(const CComplex& zC) const;
    CComplex Divide(const CComplex& zC) const;

};

#endif
