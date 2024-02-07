import bpy
import bpy.utils.previews

import os

bl_info = {
    "name": "Sample: Show Active in Outliner",
    "author": "maitakedayo",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "3D Viewport > Sidebar > ActiveObjOL",
    "description": "Addon that shows the active object in the Outliner if it is collapsed.",
    "warning": "",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "category": "Sample"
}

custom_image_collection = None

def show_active_in_outliner_and_activate_area():
    """アクティブなオブジェクトがアウトライナで折りたたまれている場合、それを表示する"""
    context = bpy.context

    active_object = context.active_object

    if active_object:
        # アクティブなオブジェクトがアウトライナで折りたたまれている場合、それを表示する
        for area in context.screen.areas:
            if area.type == 'OUTLINER':
                bpy.context.window.scene = bpy.context.scene
                bpy.ops.object.select_all(action='DESELECT')
                active_object.select_set(True)

                context.view_layer.objects.active = active_object

                # アウトライナで表示
                override = {'area': area}
                bpy.ops.outliner.show_active(override)


class SAMPLE_OT_ActiveObjOL(bpy.types.Operator): #継承
    """メニューやツールバーから呼び出すボタン追加機能(継承で差分作成), 星2Dを作るクラス"""

    bl_idname = "sample.show_active_in_outliner" #クラス変数
    bl_label = "Show Active in Outliner"
    bl_description = "Show the active object in the Outliner if it is collapsed"
    bl_options = {'REGISTER', 'UNDO'}

    # execute：オペレータが実行されたときに呼び出される
    def execute(self, context):
        show_active_in_outliner_and_activate_area()
        print("Operator executed.")
        return {'FINISHED'}

class SAMPLE_PT_ActiveObjOL(bpy.types.Panel): #継承
    """Nでボタン表示作成(継承で差分作成)"""
    bl_idname = "SAMPLE_PT_ActiveObjOL"
    bl_label = "Show Active in Outliner"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ActiveObjOL"

    def draw_header(self, context):
        """アイコン追加"""
        layout = self.layout

        layout.label(text="", icon_value=custom_image_collection["custom_icon"].icon_id)

    def draw(self, context):
        """Nでボタン表示UI"""
        layout = self.layout
        scene = context.scene

        op = layout.operator(SAMPLE_OT_ActiveObjOL.bl_idname, text="Push") #作成ボタン

classes = [
    SAMPLE_OT_ActiveObjOL,
    SAMPLE_PT_ActiveObjOL,
]

# register：アドオンのオペレータを登録し、メニューに追加
def register():
    for c in classes:
        bpy.utils.register_class(c)

    #カスタムボタンの左横に自作pngアイコンを使う
    global custom_image_collection
    custom_image_collection = bpy.utils.previews.new()
    custom_image_collection.load("custom_icon", f"{os.path.dirname(__file__)}/custom_icon.png", 'IMAGE')

    print(f"Addon '{bl_info['name']}' is now enabled.")

# unregister：アドオンのオペレータの登録を解除し、メニューから削除
def unregister():
    bpy.utils.previews.remove(custom_image_collection)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    
    print(f"Addon '{bl_info['name']}' is now disabled.")

if __name__ == "__main__":
    register()
