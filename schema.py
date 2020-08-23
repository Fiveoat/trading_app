import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database_handler import db_session, Users as UsersModel, Articles as ArticlesModel, \
    PaperTrades as PaperTradesModel, Tickers as TickersModel, \
    TickerArticleRelationships as TickerArticleRelationshipsModel, \
    PaperTradeTickerRelationships as PaperTradeTickerRelationshipsModel, Sources as SourcesModel, \
    SourceArticleRelationships as SourceArticleRelationshipsModel


class Users(SQLAlchemyObjectType):
    class Meta:
        model = UsersModel
        interfaces = (relay.Node,)


class Articles(SQLAlchemyObjectType):
    class Meta:
        model = ArticlesModel
        interfaces = (relay.Node,)


class PaperTrades(SQLAlchemyObjectType):
    class Meta:
        model = PaperTradesModel
        interfaces = (relay.Node,)


class Tickers(SQLAlchemyObjectType):
    class Meta:
        model = TickersModel
        interfaces = (relay.Node,)


class TickerArticleRelationships(SQLAlchemyObjectType):
    class Meta:
        model = TickerArticleRelationshipsModel
        interfaces = (relay.Node,)


class PaperTradeTickerRelationships(SQLAlchemyObjectType):
    class Meta:
        model = PaperTradeTickerRelationshipsModel
        interfaces = (relay.Node,)


class Sources(SQLAlchemyObjectType):
    class Meta:
        model = SourcesModel
        interfaces = (relay.Node,)


class SourceArticleRelationships(SQLAlchemyObjectType):
    class Meta:
        model = SourceArticleRelationshipsModel
        interfaces = (relay.Node,)


class CreateUser(graphene.Mutation):
    class Input:
        user_id = graphene.Int()
        name = graphene.String()
        email = graphene.String()
        last = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @classmethod
    def mutate(cls, _, args):
        user = UsersModel(first=args.get('name'), email=args.get('email'), last=args.get('username'),
                          user_id=args.get('user_id'))
        db_session.add(user)
        db_session.commit()
        ok = True
        return CreateUser(user=user, ok=ok)


class UpdateUsername(graphene.Mutation):
    class Input:
        first = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @classmethod
    def mutate(cls, _, args, context):
        query = Users.get_query(context)
        email = args.get('email')
        username = args.get('username')
        user = query.filter(UsersModel.email == email).first()
        user.username = username
        db_session.commit()
        ok = True
        return UpdateUsername(user=user, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = SQLAlchemyConnectionField(Users)
    find_user = graphene.Field(lambda: Users, user_id=graphene.Int())
    all_users = SQLAlchemyConnectionField(Users)
    ticker = SQLAlchemyConnectionField(Tickers)
    find_ticker = graphene.Field(lambda: Tickers, symbol=graphene.String())
    all_tickers = SQLAlchemyConnectionField(Tickers)

    @staticmethod
    def resolve_find_user(args, context):
        print(args)
        query = Users.get_query(context)
        user_id = args.get('user_id')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(UsersModel.user_id == user_id).first()

    @staticmethod
    def resolve_find_ticker(args, context):
        print(args)
        query = Tickers.get_query(context)
        symbol = args.get('symbol')
        return query.filter(TickersModel.symbol == symbol).first()


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    change_username = UpdateUsername.Field()


schema = graphene.Schema(query=Query, mutation=Mutations,
                         types=[Users, Articles, Tickers, Sources, TickerArticleRelationships,
                                SourceArticleRelationships, PaperTrades, PaperTradeTickerRelationships])
