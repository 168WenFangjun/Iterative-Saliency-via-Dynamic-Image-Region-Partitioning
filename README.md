# Iterative-Saliency-via-Dynamic-Image-Region-Partitioning
![image](https://github.com/168WenFangjun/Iterative-Saliency-via-Dynamic-Image-Region-Partitioning/blob/master/code-for-my-graduate-paper/test/3_95_95850.jpg)
![image](https://github.com/168WenFangjun/Iterative-Saliency-via-Dynamic-Image-Region-Partitioning/blob/master/code-for-my-graduate-paper/saliencymap/3_95_95850.png)


# Introduction 

Vison Old, Vision New. 

After reading this paper , you will get new insights of computer vision. 

For more detail information, please contact with me via gmail [168fangjunwen@gmail.com].

# Features


- computer vision 
- image saliency 
- image segmentation [image superpixel segmentation demo](http://aizaozhidao.vip/image-painter)

 
# Abstract

A  novel  object  level  saliency  model  is  proposed  in  this letter  via  iterating  saliency  classification  difference  on  dynamic  image region  partitioning.  

First,  the  model  proposed  solved  three  problems which  is  caused  by  static  background  based  methods.  Then  dynamic background  is  represented  and  computed  on  the  input  image  via dynamic  image  partitioning.  Unlike  existing  static  background  based methods,  we  calculate  saliency  difference  based  on  dynamic background  rather  than  static  image  region.  This  strategy  makes  the saliency  result  more  precisely  to  the  location  of  image  objects.  We apply  two  saliency  classification  difference  on  the  dynamic background.  

Second,  saliency  classification  difference  is  iterated  on saliency  maps  generating  by  dynamic  image  region  partitioning.  This makes  the  saliency  results  more  robust.  To  get  a  more  robust  result, the  dynamic  image  partitioning  is  operated  on  an  image  in  four directions  (i.e.,  left  to  right,  right  to  left,  top  to  bottom,  bottom  to  top). 

Third,  the  final  saliency  map  is  generated  by  combining  four  saliency maps  based  on  four  direction  scanning.  The  four  direction combination  enables  the  proposed  method  to  uniformly  highlight  the salient  object  and  simultaneously  suppress  the  background  effectively. Extensive  experiments  on  two  large  dataset  demonstrate  that  the proposed  method  performs  favorably  against  the  classic  methods  in terms of  accuracy  and efficiency. 

Index  Terms—Dynamic  image  region  partitioning,  iterating, dynamic  background,  four  direction  scanning,  saliency  map. 

In  this  letter,  we  present  a  bottom-up  object  level  saliency detection  model  by  exploiting  dynamic  image  region  partitioning, iterating  saliency  difference  and  four  direction  scanning. 

Firstly,  we get  more  precise  results  than  the  background  based  methods  with dynamic  image  region  partitioning.  

Secondly,  iterating  the  saliency classification  difference  automatically  separates  the  salient  object and  the  background.  

Thirdly,  the  four  direction  scanning  makes  our algorithm  more  robust.  

Saliency  maps  on  a  large  public  dataset demonstrate  that  the  proposed  method  can  highlight  the  whole object  region  uniformly  and  suppress  the  background  region effectively.  

In  addition,  the  proposed  method  performs  favorably against  the  classic  methods  in  accuracy,  which  shows  that  the proposed  dynamic  image  region  partitioning,  iterating  saliency classification  results  and  four  direction  scanning  are  useful  for saliency  detection.  In  the  future  work,  we  will  investigate  a  more complicated  classification  strategy  to  boost  classification  results  at different  scales  and  explore  more  applications  of  dynamic  image region  partitioning  to  other  saliency  algorithms. 




