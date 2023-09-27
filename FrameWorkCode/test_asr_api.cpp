#include <iostream>
#include <string>
#include<cstring>
// #include <curl-8.3.0/include/curl/curl.h>
#include <curl/curl.h>
#include <locale>
#include <codecvt>
#include <sstream>
#include <typeinfo>

using namespace std;


size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    // This function will be called by libcurl to write response data
    size_t total_size = size * nmemb;
    static_cast<std::string*>(userp)->append(static_cast<char*>(contents), total_size);
    return total_size;
}

string PerformPostRequest(const string& url, const string& audioFilePath) {
    CURL* curl;
    CURLcode res;
    string response_data;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if (curl) {
        // Set the URL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // Set the POST data (audio file)
        curl_httppost* post = NULL;
        curl_httppost* last = NULL;
        curl_formadd(&post, &last, CURLFORM_COPYNAME, "file", CURLFORM_FILE, audioFilePath.c_str(), CURLFORM_END);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, post);

        // Set the write callback function for response data
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);

        // Perform the POST request
        res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK) {
            cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << endl;
        }

        // Clean up
        curl_easy_cleanup(curl);
        curl_formfree(post);
        curl_global_cleanup();
    }

    return response_data;
}

int main() {
    string url = "http://localhost:5000/speech-to-text"; // Replace with your API endpoint URL
    string audioFilePath = "/home/abhay/Desktop/audio/audio.flac"; // Replace with the path to your audio file
    //    /home/abhay/MTP_NEW/data/voice_data/data1.wav
    string response = PerformPostRequest(url, audioFilePath);
    cout << response << std::endl;


    return 0;
}
// NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE



// g++ test_asr_api.cpp -lcurl