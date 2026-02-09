import 'package:dio/dio.dart';
import '../models/user_stats_model.dart';

/// Remote DataSource pour UserStats (appels API)
abstract class UserStatsRemoteDataSource {
  /// GET /users/me/stats
  ///
  /// Récupère la progression globale de l'utilisateur
  ///
  /// Returns: UserProgressionModel
  /// Throws: DioException si erreur réseau
  Future<UserProgressionModel> getUserProgression();
}

class UserStatsRemoteDataSourceImpl implements UserStatsRemoteDataSource {
  final Dio _dio;

  UserStatsRemoteDataSourceImpl(this._dio);

  @override
  Future<UserProgressionModel> getUserProgression() async {
    final response = await _dio.get('/users/me/stats');

    // L'API retourne DIRECTEMENT l'objet
    final data = response.data as Map<String, dynamic>;

    return UserProgressionModel.fromJson(data);
  }
}
