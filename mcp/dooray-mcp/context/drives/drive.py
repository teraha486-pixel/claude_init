import httpx
import server
import mcp.types as types
from adapter.drives import drive_adapter
from model.drive.response.drive import DriveBrief, DriveInfo
from utils import converter

@server.register_tool(
  description='get list of drives which is able to access.',
  inputSchema={
      "type": "object",
      "properties": {
          "query_string": {
              "type": "string",
              "description": 
              """
              plz build Query string with under fields.

              projectId={}          /* target project id */
              type={project}               /* drive type. private, project*/
              scope={}              /* if type is 'project' then 'private' or 'public' */
              state=active,archived /* saved status of drive. default=active */
              """
          }
      },
      "required": ["query_string"]
  }
)
async def get_drive_list(query_string: str) -> list[types.TextContent]:
  response: list[DriveBrief] = await drive_adapter.get_drive_list(query_string)
  return converter.convert_mcp_text_output(response)

@server.register_tool(
  description='get list of folders in specific drive.',
  inputSchema={
      "type": "object",
      "properties": {
          "drive_id": {
              "type": "string"
          },
          "query_string": {
              "type": "string",
              "description": 
              """
              plz build Query string with under fields.

              type=folder // fixed
              subTypes=root // depends on type. -> folder(root, tarsh, users), file(etc, doc, photo, movie, music, zip)
              parentId={} // parent id of the target folder
              page={}
              size={}
              """
          }
      },
      "required": ["drive_id", "query_string"]
  }
)
async def get_folder_list_in_drive(drive_id:str, query_string: str) -> list[types.TextContent]:
  response: list[DriveInfo] = await drive_adapter.get_folder_list(drive_id, query_string)
  return converter.convert_mcp_text_output(response)

@server.register_tool(
  description="dooray drive creater. Upload local file to drive env automatically.",
  inputSchema={
      "type": "object",
      "properties": {
          "drive_id": {
              "type": "string",
              "description": 
              """
              target drive id
              """
          },
          "parent_id": {
              "type": "string",
              "description": 
              """
              target folder id which is in target drive. 
              """
          },
          "file_path": {
              "type": "string",
              "description": 
              """
              local file path
              """
          },
      },
      "required": ["drive_id", "parent_id", "file_path"]
  }
)
async def upload_file_to_drive(drive_id:str, parent_id:str, file_path:str) -> list[types.TextContent]:
  response: httpx.Response = await drive_adapter.upload_file_to_drive(drive_id, parent_id, file_path)
  return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
  description = "dooray drive creater. only upload string data not file data.",
  inputSchema={
      "type": "object",
      "properties": {
          "drive_id": {
              "type": "string",
              "description": 
              """
              target drive id
              """
          },
          "parent_id": {
              "type": "string",
              "description": 
              """
              target folder id which is in drive 
              """
          },
          "file_name": {
              "type": "string",
              "description": 
              """
              The file name will be saved. default is '.md'
              """
          },
          "content": {
              "type": "string",
              "description": 
              """
              String data which is saved
              """
          },
      },
      "required": ["drive_id", "parent_id", "file_name", "content"]
  }
)
async def upload_not_file_content_to_drive(drive_id:str, parent_id:str, file_name:str, content:str) -> list[types.TextContent]:
  response: httpx.Response = await drive_adapter.upload_stream_to_drive(drive_id, parent_id, file_name, content)
  return [types.TextContent(type="text", text=response.text)]