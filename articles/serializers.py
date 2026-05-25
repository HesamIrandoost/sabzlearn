from rest_framework import serializers
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields = ['name']


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=True,
        help_text="لیست اسم تگ‌ها - اگه نباشه ساخته میشه"
    )
    
    # برای نمایش تگ‌ها موقع GET
    tags_display = TagSerializer(many=True, read_only=True, source='tags')
    
    class Meta:
        model = Article
        fields = ['slug', 'title', 'content', 'image', 'tags', 'tags_display']
    
    def validate_title(self, value):
        if Article.objects.filter(title=value).exists():
            raise serializers.ValidationError("مقاله‌ای با این عنوان قبلاً ثبت شده")
        return value
    
    def create(self, validated_data):
        tags_names = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        
        # هر تگی که بود (حتی اگه نبود) بساز یا بگیر
        for tag_name in tags_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            article.tags.add(tag)
        
        return article
    
    def update(self, instance, validated_data):
        tags_names = validated_data.pop('tags', None)
        
        # بروزرسانی فیلدهای دیگه
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # بروزرسانی تگ‌ها
        if tags_names is not None:
            instance.tags.clear()
            for tag_name in tags_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                instance.tags.add(tag)
        
        return instance



class ArticleListSerializer(serializers.ModelSerializer):
    """ لیست همه مقالات """
    author_name = serializers.SerializerMethodField()
    author_phone = serializers.SerializerMethodField()
    
    class Meta:
        model= Article
        fields = ['author_phone', 'author_name', 'slug', 'title', 'content', 'image', 'created_at']


    def get_author_name(self, obj):
        """گرفتن نام و نام خانوادگی از InstructorProfile"""
        return f"{obj.author.first_name} {obj.author.last_name}"
    
    def get_author_phone(self, obj):
        """گرفتن شماره تلفن از InstructorProfile"""
        return f"{obj.author.user.phone}"
    


class ArticleDetailSerializer(serializers.ModelSerializer):
    """  جزییات مقالات """
    tags = TagSerializer( many=True,read_only=True)

    author_name = serializers.SerializerMethodField()
    author_phone = serializers.SerializerMethodField()
    
    class Meta:
        model= Article
        fields = ['author_phone', 'author_name', 'slug', 'title', 'content', 'image', 'tags', 'created_at', 'updated_at']
        

    def get_author_name(self, obj):
        """گرفتن نام و نام خانوادگی از InstructorProfile"""
        return f"{obj.author.first_name} {obj.author.last_name}"
    
    def get_author_phone(self, obj):
        """گرفتن شماره تلفن از InstructorProfile"""
        return f"{obj.author.user.phone}"
    

