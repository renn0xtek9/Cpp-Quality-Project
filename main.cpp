#include <iostream>
#include <queue>
#include <memory>
#include <opencv2/opencv.hpp>
struct whatever
{ 
    int what;
    double ever;
};


cv::Mat CreateBlankImage()
{
    cv::Mat img(600,800,CV_8UC(3));
    return img;
}
void DrawNumberOnFrame(cv::Mat img, int number)
{
    cv::Point origin;
    origin.x=100;
    origin.y=200;
    std::string number_as_str=std::to_string(number);
    cv::putText(img,number_as_str ,origin, cv::FONT_HERSHEY_COMPLEX_SMALL, 10.0, cv::Scalar(255,0,255),1,CV_AA); 
    
}

cv::Mat GetFrameFromSubscriber(int index)
{
    cv::Mat ret=CreateBlankImage();
    DrawNumberOnFrame(ret,index);
    return ret;
}



int main(int argc, char **argv) {
    uint maxsize=3  ;    
    std::queue<std::shared_ptr<cv::Mat>> finite_queue;

    for(int i=0;i<15;i++)
    {   
        std::unique_ptr<cv::Mat> mat_ptr=std::make_unique<cv::Mat>(GetFrameFromSubscriber(i));
        finite_queue.push(std::move(mat_ptr));
        if (finite_queue.size()>maxsize)
        {
            finite_queue.pop();
        }
        std::shared_ptr<cv::Mat> display_mat=finite_queue.front();
        cv::imshow("Display",*display_mat);
        cv::waitKey(0);
    }
    return 0;
}
