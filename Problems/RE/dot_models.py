from __future__ import print_function, division
import sys,os
sys.path.append(os.path.abspath("."))
sys.dont_write_bytecode = True
from Problems.RE.template import Graph
__author__ = 'george'

def CSServices():
  resources = ["Service Resources", "Web Server", "Feedback Form Software", "Web Software",
                 "Strategic Blue Print", "Feedback", "Web Site Content", "Phone Library of Recorded Messages",
                 "Feedback1"]
  containers = ["CS", "Fund Development and Marketing", "Provincial government",
                "CS Technology Services", "CS Service", "Web Service", "Phone Service",
                "Counselling Management", "PHL Service", "Parents", "IT Department",
                "Web Task Force", "CS Web Services", "CS Phone Services", "PHL Phone Services",
                "PHL Web Services", "Counselling", "Kids and Youth"]
  graph = Graph.from_dot("CSServices", "Problems/RE/graphviz/stage1/CSServices.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSComplex():
  resources = []
  containers = ["Parents", "CS Service", "Phone Service", "PHL Phone Services",
                "CS Technology Services", "CS Phone Services", "Community Resource",
                "Provincial government", "Web Service", "PHL Web Services",
                "Public Education Program", "CS Web Services", "Not For Profit Partners",
                "General Public", "Research Partners", "IT Department", "IT Company"]

def CSCounselling():
  containers = ["Counselling Resource Acquisition/Maintenance", "Counsellors Union",
                "Counselling Employee", "Counselling Public/Internal Relations",
                "Marketing and Fund Development", "Counselling Clinical Supervision Target",
                "Counselling Training", "Counselling Information Provider", "Parents",
                "Kids and Youth", "Counselling", "Counselling Management", "IT Department",
                "Web Counselling", "Activity Manager" ,"Phone System", "Voice Counselling"
                "Research Partners", "CS Services", "CS"]
  resources = ["Information in E-Library", "Information Binders at Stations",
               "Resources in the Library", "Tapes", "Tape Recording Technology", "Salary",
               "Counselling Workshops", "Double Headsets", "Training CDs", "Information/Resources",
               "Counselling Policies", "Web Moderator Meetings", "Counsellor Experience",
               "Caller Statistics", "Web Site Content", "Feedback"]
  graph = Graph.from_dot("CSCounselling", "Problems/RE/graphviz/stage1/CSCounselling.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSCounsellingManagement():
  containers = ["CS", "Clinical Supervision", "Counselling Management", "Counselling Management Technical Encouraging",
                "Counselling Human Resource Managment", "Counselling", "CS Technology Services",
                "Counselling Scheduling", "Director Enterprise/Blue Pumpkin", "Counselling Training Management"
                "Counselling Manager", "IT Department"]
  resources = ["Counselling Resources", "Double Head Set", "Salary", "Counselling Workshops"
               ,"Counselling Policies", "Web Moderator Meetings", "Call Statistics",
               "Historical Data of Call Volumes"]
  graph = Graph.from_dot("CSCounsellingManagement", "Problems/RE/graphviz/stage1/CSCounsellingManagement.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSCounsellingManagementSD():
  containers = ["CS", "Clinical Supervision", "Counselling Management", "Counselling Management Technical Encouraging",
                "Counselling Human Resource Managment", "Counselling", "CS Technology Services",
                "Counselling Scheduling", "Director Enterprise/Blue Pumpkin", "Counselling Training Management"
                "Counselling Manager", "IT Department"]
  resources = ["Counselling Resources", "Double Head Set", "Salary", "Counselling Workshops"
               ,"Counselling Policies", "Web Moderator Meetings", "Call Statistics",
               "Historical Data of Call Volumes"]
  graph = Graph.from_dot("CSCounsellingManagementSD", "Problems/RE/graphviz/stage1/CSCounsellingManagementSD.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSCounsellingSD():
  containers = ["Counselling Resource Acquisition/Maintenance", "Counsellors Union",
                "Counselling Employee", "Counselling Public/Internal Relations",
                "Marketing and Fund Development", "Counselling Clinical Supervision Target",
                "Counselling Training", "Counselling Information Provider", "Parents",
                "Kids and Youth", "Counselling", "Counselling Management", "IT Department",
                "Web Counselling", "Activity Manager" ,"Phone System", "Voice Counselling"
                "Research Partners", "CS Services", "CS", "Counselling Support to Counselling"]
  resources = ["Information in E-Library", "Information Binders at Stations",
               "Resources in the Library", "Tapes", "Tape Recording Technoloyg", "Salary",
               "Counselling Workshops", "Double Headsets", "Training CDs", "Information/Resources",
               "Counselling Policies", "Web Moderator Meetings", "Counsellor Experience",
               "Caller Statistics", "Web Site Content", "Feedback"]
  graph = Graph.from_dot("CSCounsellingSD", "Problems/RE/graphviz/stage1/CSCounsellingSD.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSFDandMarketing():
  containers = ["CS", "CS Services", "Individual donor", "SA Program", "CEO +CFO", "Not for Profit Partners",
                "VP Marketing and Fund Development", "Counselling", "Regional Offices", "IT department"]
  resources = ["Free advertisement", "Sponsor Logo", "Funds", "Agreement", "Exclusive Brand and Logo use",
               " Free services", "Sponsor partner\ncontacts", "Sponsor partner\ncontacts1", "Sponsor partner\ncontacts2",
               "Single charitable registration number", "Single charitable registration number1",
               "National Marketing Strategy ", "Sponsor Logo", "Donor/Accounting Database", "Promotion Resources"]
  graph = Graph.from_dot("CSFDandMarketing", "Problems/RE/graphviz/stage1/CSFD and Marketing.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSFDandMarketingSD():
  containers = ["CS", "CS Services", "Individual donor", "Corporate Sponsor", "Donor Technology",
                "Marketing", "Corporate Partner Management", "Fund Development", "CEO +CFO", "SA Program",
                "Counselling", "Regional Offices", "HR for Marketing and Fundraising staff", "IT department",
                "Provincial government", "Not for Profit Partners", "Regional\nContact management"]
  resources = ["Free advertisement", "Funds", "Sponsor Logo", "Agreement", " Free services", "Sponsor partner\ncontacts"
               "Promotion Resources", "Single charitable registration number", "National Event Calendar",
               "Donor/Accounting Database"]
  graph = Graph.from_dot("CSFDandMarketingSD", "Problems/RE/graphviz/stage1/CSFD and MarketingSD.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSITDepartment():
  containers = ["CS", "Counselling Management", "Counselling", "IT Company",
                "Pro Bono Company", "CS Services", "FD & M"]
  resources = ["IT Resources", "Web Server", "Software", "Free Software",
               "Free Hardware", "Hardware", "Free Web Server", "Oracle",
               "Feedback Form Software", "Web Software", "Web Server1",
               "Donor/Accounting Data Base", "Upgrades", "Free Upgrades"]
  graph = Graph.from_dot("CSITDepartment", "Problems/RE/graphviz/stage1/CSITDepartment.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSSAProgram():
  containers = ["CS", "Student Ambassador Volunteer", "Student Ambassador",
                "Marketing and Fund Development", "Schools"]
  resources = ["Promotion Resources", "Promotion Resources1", "Speaches"]
  graph = Graph.from_dot("CSSAProgram", "Problems/RE/graphviz/stage1/CSSAProgram.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def CSSimplified():
  containers = ["General Public", "Corporate employee", "Individual donor", "Corporate Sponsor", "Donor Technology",
                "Not for Profit Partners", "Marketing and Fund Development", "Corporate Partner Management",
                "Research Partners", "CEO +CFO", "Public Education Program", "Regional\nContact management",
                "Provincial government", "Community Resource", "CS", "Regional Offices", "Student Ambassador Volunteer",
                "IT Company", "IT Department", "Counselling Employee", "SA Program", "Student Ambassador Coordinator",
                "Student Ambassador", "Schools", "Parents", "Pro-bono Partners", "Counselling Management",
                "Director Enterprise/Blue Pumpkin", "CS Technology Services", "Web Task Force", "Kids and Youth",
                "Phone System", "Counselling", "Counsellors Union", "Counselling Manager"]
  resources = ["Information", "Sponsor Logo", " Free services", "Sponsor partner\ncontacts", "Agreement", "Funds",
               "Donor/Accounting Data Base", "Single charitable registration number", "Service Resources", "IT Resources",
               "Promotion Resources", "Promotion Resources1", "Speaches", "Web Server", "Web Server1", "Software", "Hardware",
               "Upgrades", "Feedback Form Software", "Web Software", "Free Web Server", "Free Upgrades", "Free Hardware",
               "Free Software", "Oracle", "Free advertisement", "Counsellor Experience", "Web Site Content", "Double Head Set",
               "Counselling Workshops", "*Salary", "Counselling Policies", "Web Moderator Meetings", "Call Statistics",
               "Phone Library of Recorded Messages", "Strategic Blue Print", "Caller Statistics", "Feedback", "Feedback1",
               "Tape Recording Technology", "Training CDs", "Tapes", "Historical Data of Call Volumes"]
  graph = Graph.from_dot("CSSimplified", "Problems/RE/graphviz/stage1/CSSimplified.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def KidsAndYouth():
  containers = ["CS", "CS web technology"]
  resources = ["Feedback"]
  graph = Graph.from_dot("Kids and Youth", "Problems/RE/graphviz/stage1/Kids and Youth.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def Parents():
  containers = ["CS", "PHL web technology"]
  resources = ["Feedback", "Phone Library of Recorded Messages", "Phone Library of Recorded Messages1"]
  graph = Graph.from_dot("Parents", "Problems/RE/graphviz/stage1/Parents.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage1/%s.json"%graph.name)
  return graph

def OOOChatRooms():
  resources = []
  containers = ["CS Technology Services", "CS Service", "Web Service", "CS Web Services",
                "Counselling", "Counselling Employee", "Web Counselling"]
  graph = Graph.from_dot("OOOChatRooms", "Problems/RE/graphviz/stage2/chat_room.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage2/%s.json"%graph.name)
  return graph

def DelayModeratedBulletinBoard():
  containers = ["CS Technology Services", "CS Service", "Web Service", "CS Web Services",
                "Counselling Employee", "Counselling", "Web Counselling"]
  resources = []
  graph = Graph.from_dot("DelayModeratedBulletinBoard", "Problems/RE/graphviz/stage2/Delay Moderated Bulletin Board.gv", resources, containers)
  #Graph.json(graph, "Problems/RE/json/stage2/%s.json"%graph.name)
  return graph
