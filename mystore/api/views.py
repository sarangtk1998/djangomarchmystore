from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ViewSet,ModelViewSet

from api.models import Products,Carts,Reviews
from api.serializers import ProductSerializer,ProductModelSerializer,UserSerializer,CartSerializer,ReviewSeializer

from rest_framework.decorators import action

from rest_framework import permissions,authentication


class ProductView(APIView):

    def get(self,request,*args,**kw):

        qs = Products.objects.all()

        serializer = ProductSerializer(qs,many=True)

        return Response(data=serializer.data)
    
    def post(self,request,*args,**kw):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)

            Products.objects.create(**serializer.validated_data)

            return Response(data=serializer.data)
        
        else:
            return Response(serializer.errors)

class ProductdetailsView(APIView):

    def get(self,request,*args,**kw):

        print(kw)

        id = kw.get("id")

        qs = Products.objects.get(id=id)
        serializer = ProductSerializer(qs,many=False)

        return Response(data=serializer.data)

    def put(self,request,*args,**kw):

        id = kw.get('id')

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            Products.objects.filter(id=id).update(**request.data)

            return Response(data=serializer.data)
        
        else:
            return Response(data=serializer.errors)
    
    def delete(self,request,*args,**kw):

        id = kw.get('id')

        Products.objects.filter(id=id).delete()

        return Response(data='object deleted')
    


# class ProductViewsetView(ViewSet):

#     def list(self,request,*args,**kw):

#         qs = Products.objects.all()

#         serializer = ProductSerializer(qs,many=True)

#         return Response(data=serializer.data)
    

#     def create(self,request,*args,**kw):

#         serializer = ProductModelSerializer(data=request.data)
        
#         if serializer.is_valid():
#              serializer.save()
#              return Response(data=serializer.data)
        
#         else:
#             return Response(data=serializer.errors)
        
#     def retrieve(self,request,*args,**kw):

#         id = kw.get('pk')
#         print(kw)

#         qs = Products.objects.get(id=id)
#         serializer = ProductModelSerializer(qs,many=False)
#         return Response(data=serializer.data)


#     def destroy(self,request,*args,**kw):

#         id = kw.get('pk')

#         Products.objects.filter(id=id).delete()

#         return Response(data='deleted')
    

#     def update(self,request,*args,**kw):

#         id = kw.get('pk')

#         obj = Products.objects.get(id=id)

#         serializer = ProductModelSerializer(data=request.data,instance=obj)

#         if serializer.is_valid():

#             serializer.save()

#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
        

#     @action(methods=['GET'],detail=False)
#     def categories(self,request,*args,**kw):

#         res = Products.objects.values_list('category',flat=True).distinct()

#         return Response(data=res)

#     @action(methods=['GET'],detail=False)
#     def des(self,request,*args,**kw):

#         res = Products.objects.values_list('description',flat=True).distinct()

#         return Response(data=res)
    

class UserView(ViewSet):

    def create(self,request,*args,**kw):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(data=serializer.data)
        
        else:
            return Response(serializer.errors)
    
    

class ProductModelViewset(ModelViewSet):

    serializer_class = ProductModelSerializer
    queryset = Products.objects.all()
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'],detail=True)
    def addto_cart(self,request,*args,**kw):

        id = kw.get("pk")
        item = Products.objects.get(id=id)
        user = request.user
        user.carts_set.create(products=item)

        return Response(data='item added to cart')
    
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kw):

        user = request.user
        id = kw.get('pk')

        object = Products.objects.get(id=id)

        serializer = ReviewSeializer(data=request.data)

        if serializer.is_valid():

            serializer.save(product=object,user=user)

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)    

    @action(methods=['GET'],detail=True)
    def reviews(self,request,*args,**kw):

        # id = kw.get("pk")
        # product = Products.objects.get(id=id)

        product = self.get_object()

        qs = product.reviews_set.all()

        serializer = ReviewSeializer(qs,many=True)
        return Response(serializer.data)





class CartView(ModelViewSet):

    serializer_class = CartSerializer
    queryset = Carts.objects.all()

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return self.request.user.carts_set.all()   #Carts.objects.filter(user=self.request.user)

    # def list(self,request,*args,**kw):

    #     qs = request.user.carts_set.all()

    #     serializer = CartSerializer(qs,many=True)

    #     return Response(data=serializer.data)

    # def post(self,request,*args,**kw):

    #     id = kw.get("id")
    #     item = Products.objects.get(id=id)
    #     user = request.user
    #     user.carts_set.create(products=item)

    #     return Response(data='item added to cart')


class ReviewDeleteView(APIView):

    def delete(self,request,*args,**kw):

        id = kw.get('pk')

        Reviews.objects.filter(id=id).delete()

        return Response(data='review deleted')
