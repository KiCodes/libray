from rest_framework import serializers
from .models import Author, Book, Publisher, Borrower, Loan

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        # get author and publisher json data from nested response
        author_data = validated_data.pop('author')
        publisher_data = validated_data.pop('publisher')
        
        author, created = Author.objects.get_or_create(**author_data)
        print(f'was author created ---> {created}')
        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        print(f'was publisher created ---> {created}')
        
        book = Book.objects.create(author=author, publisher=publisher, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        publisher_data = validated_data.pop('publisher')
        
        author, created = Author.objects.get_or_create(**author_data)
        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        
        instance.author = author
        instance.publisher = publisher
        instance.title = validated_data.get('title', instance.title)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.save()
        return instance

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    borrower = BorrowerSerializer()

    class Meta:
        model = Loan
        fields = '__all__'

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        borrower_data = validated_data.pop('borrower')

        author_data = book_data.pop('author')
        publisher_data = book_data.pop('publisher')
        
        author, created = Author.objects.get_or_create(**author_data)
        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        
        book, created = Book.objects.get_or_create(author=author, publisher=publisher, **book_data)
        borrower, created = Borrower.objects.get_or_create(**borrower_data)
        
        loan = Loan.objects.create(book=book, borrower=borrower, **validated_data)
        return loan

    def update(self, instance, validated_data):
        book_data = validated_data.pop('book')
        borrower_data = validated_data.pop('borrower')

        author_data = book_data.pop('author')
        publisher_data = book_data.pop('publisher')
        
        author, created = Author.objects.get_or_create(**author_data)
        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        
        book, created = Book.objects.get_or_create(author=author, publisher=publisher, **book_data)
        borrower, created = Borrower.objects.get_or_create(**borrower_data)

        instance.book = book
        instance.borrower = borrower
        instance.loan_date = validated_data.get('loan_date', instance.loan_date)
        instance.return_date = validated_data.get('return_date', instance.return_date)
        instance.save()
        return instance
