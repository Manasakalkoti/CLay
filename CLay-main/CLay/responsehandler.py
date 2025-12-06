from mitmproxy import http
import logging


# from lists import *
# from utility import *
# from config import *

from CLay.lists import *
from CLay.utility import *
from CLay.config import *


class ResponseHandler:
    def __init__(self, flow):
        try:
            self.flow = flow
            self.content_type = contentCheck(self.flow.response.headers)
            self.main()
        except Exception as e:
            logging.error('Error: init responseHandler %s', e)

    def main(self):
        try:
            # detection
            self.detectResponse()

            # clear informative information
            self.filterResponse()

            # add false informative information
            self.deceptResponse()
        except Exception as e:
            logging.error('Error: main responseHandler %s', e)

    def detectResponse(self):
        try:
            self.detectLocationRedirection()
        except Exception as e:
            logging.error('Error: detectResponse %s', e)

    def detectLocationRedirection(self):
        try:
            response_code = self.flow.response.status_code
            if (response_code >= 300 and response_code < 400):
                response_headers = self.flow.response.headers
                if ("Location" in response_headers):
                    target_domain = extract_domain(configure.read_config().get("target"))
                    location_domain = extract_domain(response_headers["Location"])
                    if (target_domain == location_domain):
                        response_headers["Location"] = extract_path_and_more(response_headers["Location"])
                        self.flow.response.text = ""
        except Exception as e:
            logging.error('Error: detectLocationRedirection %s', e)

    def filterResponse(self):
        try:
            # clear html comments
            val = configure.user_preference.get("filter_comment")
            if val is True:
                self.filterComment()
            elif not isinstance(val, bool):
                logging.error('Error value of filter_comment')

            # clear informative response headers
            val2 = configure.user_preference.get("filter_response_header")
            if val2 is True:
                self.filterResponseHeaders()
            elif not isinstance(val2, bool):
                logging.error('Error value of filter_response_header')
        except Exception as e:
            logging.error('Error: filterResponse %s', e)

    def deceptResponse(self):
        try:
            # add headers
            val3 = configure.user_preference.get("add_decoy_header")
            if (val3 is True) and ("headers" in configure.deception_data):
                deception_headers = configure.deception_data["headers"]
                for key, value in deception_headers.items():
                    if isinstance(value, list):
                        value = value[-1]
                    self.addHeader(key, value)
            elif not isinstance(val3, bool):
                logging.error('Error value of add_decoy_header')

            # add cookies
            val4 = configure.user_preference.get("add_decoy_cookie")
            if (val4 is True) and ("cookies" in configure.deception_data):
                deception_cookies = configure.deception_data["cookies"]
                for key, value in deception_cookies.items():
                    if isinstance(value, list):
                        value = value[-1]
                    self.addCookie(key, value)
            elif not isinstance(val4, bool):
                logging.error('Error value of add_decoy_cookie')

            # add comments
            if ("add_decoy_comment" in configure.user_preference):
                adc = configure.user_preference.get("add_decoy_comment", {})
                status = adc.get("status")
                if status is True:
                    self.addDecoyComment()
                elif not isinstance(status, bool):
                    logging.error('Error value of add_decoy_comment')

            # replace error page
            val5 = configure.user_preference.get("error_template_changing")
            if val5 is True:
                self.templateChanging()
            elif not isinstance(val5, bool):
                logging.error('Error value of error_template_changing')
        except Exception as e:
            logging.error('Error: deceptResponse %s', e)

    def addDecoyComment(self):
        try:
            for c in configure.user_preference["add_decoy_comment"]["decoy_comments"]:
                decoy_comment = c["comment"]
                url_target_paths = c["url_target_paths"]
                addComment(self.flow, decoy_comment, url_target_paths)
        except Exception as e:
            logging.error('Error: addDecoyComment %s', e)


    def addHeader(self, key, value):
        try:
            if key == "Set-Cookie":
                expire = 3600
                others = "; path=/; httponly"

                # if you want to create session, use this
                value = createCookieString(key=value, others=others)

                # if you want to create a cookie with expire date, use this
                # value = createCookieString(key=value, expire=expire, others=others)

                # .add => adding a new header with the same name without overwrite the old one
                self.flow.response.headers.add(key, value)
            else:
                # adding a new header, but will overwrite the old one if any
                self.flow.response.headers[key] = value
        except Exception as e:
            logging.error('Error: addHeader %s', e)

    def addCookie(self, key, value):
        try:
            request_cookies = self.flow.request.cookies
            response_cookies = self.flow.response.cookies

            if (key not in request_cookies) and (key not in response_cookies):
                cookie_value = createCookieString(key, value=value)
                cookie_header = "Set-Cookie"
                self.addHeader(cookie_header, cookie_value)

        except Exception as e:
            logging.error('Error: addCookie %s', e)

    # clear all informative header
    def filterResponseHeaders(self):
        try:
            response_headers = self.flow.response.headers

            # get all informative headers from the response headers
            informative_headers = set(response_headers).intersection(DANGER_HEADERS)

            # remove the informative headers from the response headers
            for i in informative_headers:
                # print("DELETED HEADER", i, response_headers[i], sep=": ")
                del response_headers[i]
        except Exception as e:
            logging.error('Error: filterResponseHeaders %s', e)

    # remove any html comment
    def filterComment(self):
        try:
            if (self.content_type in HTML_CONTENT_TYPES):
                # original pattern
                # pattern = re.compile(r'<!--(.*?)-->|\/\/[^\r\n]*|\/\*(.*?)\*\/', re.DOTALL)

                content = self.flow.response.content.decode('utf-8')
                modified_content = clearCommentInHTML(content)
                self.flow.response.content = modified_content.encode('utf-8')
            elif (self.content_type in JAVASCRIPT_CONTENT_TYPES):
                pass
            elif (self.content_type in CSS_CONTENT_TYPES):
                pass
        except Exception as e:
            logging.error('Error: filterComment %s', e)

    def templateChanging(self):
        try:
            response_code = self.flow.response.status_code
            # if response code is 401, 403, 404, or 500 return corresponding error page
            if response_code in HTTP_STATUS_CODES:
                self.flow.response = http.Response.make(
                    response_code,
                    responseTemplating(response_code),
                    {
                        "Content-Type": "text/html"
                    }
                )
        except Exception as e:
            logging.error('Error: templateChanging %s', e)
