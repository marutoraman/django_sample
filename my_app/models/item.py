from sell.models.item_stock import ItemStockModel
from sell.models.mercari_category import MercariCategoryModel
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import ulid
from ulid.api import default
from users.models import User


# 商品データモデル
class ItemModel(models.Model):
    # idはデフォルトではなく、ulidを生成するようにした方がセキュリティ上良い。デフォルトのintの連番だと容易に推測されてしまう
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True)
    title = models.CharField("商品名", max_length=128, null=False)
    description = models.TextField("説明", null=True, default="",blank=True)

    # 作成日時、更新日時は基本的に全てのテーブルにあった方がよい
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    # userは外部キーで紐づける
    user = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table='mercari_item' # table名は明示的に指定する方がわかりやすい
