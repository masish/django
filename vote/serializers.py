from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import Game, User, Player, Vote
from accounts.serializer import UserSerializer
from datetime import datetime, timezone
import pytz
from pytz import timezone


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    member = PlayerSerializer(many=True)
    first_scorer = PlayerSerializer(many=False)

    # vote = serializers.PrimaryKeyRelatedField(many=True, queryset=Vote.objects.all())

    class Meta:
        model = Game
        fields = "__all__"


class VoteReadSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    player = PlayerSerializer(read_only=True)
    game = GameSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'user', 'game', 'player')


class VoteCtrlSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # player = PlayerSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'user', 'game', 'player')

    # 更新の場合は game を表示専用にして更新させない(投票の対象ゲームが変わっては困る)
    def get_extra_kwargs(self):

        # アクションを取得
        extra_kwargs = super(VoteCtrlSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        # 更新なら game を表示専用にして Update させない
        if action in ['update', 'partial_update']:
            kwargs = extra_kwargs.get('game', {})
            kwargs['read_only'] = True
            extra_kwargs['game'] = kwargs

        return extra_kwargs

    """
    バリデーション
    """
    def validate_game(self, game):

        """
        投票できる期限を過ぎていないか確認。
        """
        if game.was_vote_closed():
            raise serializers.ValidationError("試合開始時刻を過ぎています。")

        """
        新規登録の場合、既にユーザーが投票済みではないか確認。
        """
        request = self._context["request"]._request
        if request.method == "POST":
            vote = Vote.objects.filter(game=game.id, user=request.user.id)
            if len(vote) > 0:
                raise serializers.ValidationError("既に投票済みです。")

        return game

    def validate_vote_result(self, vote_result):
        # ユーザーはvote_resul設定させない。
        raise serializers.ValidationError("vote_resultは設定できません。")


class UserSerializer(serializers.ModelSerializer):
    vote = serializers.PrimaryKeyRelatedField(many=True, queryset=Vote.objects.all())

    class Meta:
        model = User
        fields = ('username', 'vote')
