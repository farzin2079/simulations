from rest_framework import serializers
from auctions.models import Listing, Bids, User, Categorys, Comment



class CategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Comment
        fields = '__all__'
    
class BidsSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Bids
        fields = '__all__'

class ListingSerialazer(serializers.ModelSerializer):
    add_user = UserSerializer(many=False)
    bids = BidsSerializer(many=False)
    category = CategorysSerializer(many=False)
    comment = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = '__all__'
        
    def get_comment(self, obj):
        comment = obj.comment_active.all()
        serializers = CommentSerializer(comment, many=True)
        return serializers.data