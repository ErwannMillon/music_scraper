from string import Template
from email import header
import glob
import pandas as pd
import os
import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
cyanite_url = "https://api.cyanite.ai/graphql"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjozMjEsInVzZXJJZCI6MTA1MDksImFjY2Vzc1Rva2VuU2VjcmV0IjoiYzNjNDVhYjExYmE5YmZhYzdmZDNhYjVhM2E0ZmYwYzNhODhkMDZkMjlkOTEzYjVhMGI2MTUwYTEyODc2MDNmZiIsImlhdCI6MTY1ODAxNDExMn0.K_zNC_cAgcPKxlOqyyjXuvKnq_cHkoDsS0ZcxvG1QvU"
auth_str = "Bearer " + api_token

class UploadQuery:
	def __init__(self):
		upload_request_string = """
		mutation fileUploadRequest {
			fileUploadRequest {
			id
			uploadUrl
			}
		}
		"""
		self.headers = {
			"Authorization": "Bearer " + api_token,
			"Content-Type": "application/json"
		}
		self.body = json.dumps(
			{
				"query" : upload_request_string
			}
		)	

class LibraryCreateQuery:
	def __init__(self, file_path, file_upload_request_id):
		request_string = """
		  mutation LibraryTrackCreate($input: LibraryTrackCreateInput!) {
    libraryTrackCreate(input: $input) {
      ... on LibraryTrackCreateError {
        message
      }
      ... on LibraryTrackCreateSuccess {
        createdLibraryTrack {
          __typename
          id
        }
      }
    }
  }
		"""
		self.file_path = file_path
		self.filename = file_path[file_path.rfind("/") : file_path.find(".mp3")]
		self.headers = {
			"Authorization": "Bearer " + api_token,
			"Content-Type": "application/json"
		}
		self.body = json.dumps(
			{
				"query" : request_string,
				"variables" : {
					"input" : {
						"title" : self.filename,
						"uploadId" : file_upload_request_id
					}
				}
			}
		)	
# s = requests.Session()
# s.request("POST", cyanite_url, )
# print(req)
class GetTrackQuery:
	def __init__(self, id) -> None:
		self.request_string = Template("""
	query LibTrack{
	libraryTrack(id : $id){
    ...on LibraryTrack{
      audioAnalysisV6 {
        ...on AudioAnalysisV6Finished {
          result {
            segments {
              representativeSegmentIndex,
              timestamps
            }
          }
        }
      }
    }
    ...on LibraryTrackNotFoundError{
      message
    }
  }
}
		""")
		
		self.headers = {
			"Authorization": "Bearer " + api_token,
			"Content-Type": "application/json"
		}
		self.body = json.dumps(
			{
				"query" : self.request_string.substitute(id=id),
			}
		)	

def upload_file(file_path):
	upload_query = UploadQuery()
	upload_request = requests.post(cyanite_url, data=upload_query.body, headers=upload_query.headers)
	upload_request = upload_request.json()["data"]["fileUploadRequest"]
	id, url = (upload_request["id"], upload_request["uploadUrl"])
	with open(file_path, "rb") as file_stream:
		upload_response = requests.put(url, data=file_stream, headers={
			"Content_Length" : str(os.path.getsize(file_path))
		})
	print("upload_response: ", upload_response)
	return(id, url)
def add_to_lib(file_path):
	upload_id, upload_url = upload_file(file_path)
	print(upload_id)
	add_lib_request = LibraryCreateQuery(file_path, upload_id)
	add_lib_response = requests.post(cyanite_url, data=add_lib_request.body, headers = add_lib_request.headers)
	id = add_lib_response.json()["data"]['libraryTrackCreate']['createdLibraryTrack']["id"]
	print(id)
	return id

def add_db_to_lib(folder, csv_file="files_in_library.csv"):
	if os.path.exists(csv_file):
		path_and_id = pd.read_csv(csv_file, index_col=0)
		# print(path_and_id)
	else:
		path_and_id = pd.DataFrame(columns=["path", "id"])
	# print(path_and_id)
	for i, file in enumerate(glob.glob(folder + "/*")):
		if file in path_and_id["path"].values:
			print("duplicate in add_db")
			continue
		cyanite_id = add_to_lib(file)
		path_and_id.loc[len(path_and_id)] = [file, idf]
	path_and_id.to_csv(csv_file)
def get_analysis(library_id):
	# test_id = "MTA1MDkvM2U1M2YwNjUtNzgxNS00ZjE0LWEwZGUtYzU4ZTRlOTViNDQy"
	# headers = {
	# 	"Authorization": "Bearer " + api_token,
	# 	"Content-Type": "application/json"
	# }
	# test_request = """libraryTrack(id: "MTA1MDkvM2U1M2YwNjUtNzgxNS00ZjE0LWEwZGUtYzU4ZTRlOTViNDQy") {
	# 	title
	# } 
	# """
	# body = {
	# 	"query" : test_request
	# }
	query = GetTrackQuery("9539998")
	response = requests.post(cyanite_url, data=query.body, headers=query.headers)
	# response = requests.post(cyanite_url, data=json.dumps(body), headers=headers)
	segment_data = response.json()["data"]["libraryTrack"]["audioAnalysisV6"]["result"]["segments"]
	segment_index = segment_data["representativeSegmentIndex"]
	segment_index = segment_index - 1 if segment_index > 0 else segment_index
	segment_start = segment_data["timestamps"][segment_index]
	print(segment_start)
	# pp.pprint(response.json())
	# id = add_to_lib("./energy_source.mp3")
	# analysis_request()
add_db_to_lib("./audio_files")
get_analysis(None)
