from typing import Optional

class CKGNode:
  def __init__(self, uid: str, type: str, name: str, content: str = ""):
    self.uid = uid
    self.type = type  # function, file, folder, repo
    self.name = name
    self.content = content
    self.owner: Optional['CKGNode'] = None
    self.children: list['CKGNode'] = []
    self.metadata: dict = {}

  def __str__(self):
    return f"CKGNode(uid={self.uid}, type={self.type}, name={self.name})"

  def __repr__(self):
    return f"CKGNode(uid={self.uid}, type={self.type}, name={self.name}), content={self.content}, owner={self.owner}, children={self.children}, metadata={self.metadata}"