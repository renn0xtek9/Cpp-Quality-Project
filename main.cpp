#include <iostream>
#include <queue>
#include <memory>
#include <opencv2/opencv.hpp>
struct whatever {
    int what;
    double ever;
};

cv::Mat CreateBlankImage()
{
    cv::Mat mat_ptr ( 600,800,CV_8UC ( 3 ) );
    return mat_ptr;
}

void DrawNumberOnFrame ( cv::Mat& img, int number )
{
    cv::Point origin;
    origin.x=100;
    origin.y=200;
    std::string number_as_string=std::to_string ( number );
    cv::putText ( img,number_as_string,origin, cv::FONT_HERSHEY_COMPLEX_SMALL, 10.0, cv::Scalar ( 255,0,255 ),1,CV_AA );
}

cv::Mat GetFrameFromSubscriber ( int index )
{
    cv::Mat ret=CreateBlankImage();
    DrawNumberOnFrame ( ret,index );
}

int main ( int argc, char **argv )
{
//     uint maxsize=3  ;
//     std::queue<cv::Mat> finite_queue;
//     std::shared_ptr<cv::Mat> m_frameptr;

    for ( int i=0; i<15; i++ ) {
        /*if (mat1)
        {
            std::cout<<"deal";
            mat1->release();
            mat1->deallocate();
            delete mat1;
            mat1=nullptr;

        }*/
//         std::unique_ptr<int> pt
//         GetFrameFromSubscriber(mat1,i);
        cv::Mat mat=GetFrameFromSubscriber ( i );
        std::cout<<"i"<<i<<"mat"<<&mat<<std::endl;
        cv::imshow ( "mat_ptr",mat );
//        cv::waitKey(0);
//         m_frameptr=stnew cv::Mat(mat1->clone());
//         m_frameptr=std::shared_ptr <cv::Mat>(new cv::Mat(mat1->clone()));
        /*
        finite_queue.emplace((*m_frameptr).clone());
        if (finite_queue.size()>maxsize)
        {
            finite_queue.front().release();
            finite_queue.pop();
        }
        cv  ::Mat clonedMat=finite_queue.front().clone();
        std::unique_ptr<cv::Mat> display_mat=std::make_unique<cv::Mat>(clonedMat);
        cv::imshow("Display",*display_mat);
        cv::waitKey(0);
        */
    }
    return 0;
}
