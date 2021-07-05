#!/usr/bin/awk -f
BEGIN{
    FS="\t";
    OFS="\t";
    TP=0;
    TN=0;
    FP=0;
    FN=0;
}
{
    if($2>0.5){
        if($3==1){TP+=1;}
        else{FP+=1;}
    }
    else{
        if($3==0){TN+=1;}
        else{FN+=1;}
    }
}
END{
    PRECISION=TP/(FP+TP);
    RECALL=TP/(TP+FN);
    ACCURACY=(TP+TN)/(FP+TP+FN+TN);
    print PRECISION, RECALL, ACCURACY;
}