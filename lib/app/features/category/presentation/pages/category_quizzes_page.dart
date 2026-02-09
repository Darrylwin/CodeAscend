import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../data/models/category_model.dart';

/// Page listant les quizzes d'une catégorie (optionnelle, list & filter)
class CategoryQuizzesPage extends StatelessWidget {
  final String categoryId;
  final String? level;
  final List<QuizSummaryModel>? quizzes;

  const CategoryQuizzesPage({
    super.key,
    required this.categoryId,
    this.level,
    this.quizzes,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final greyColor = isDarkMode ? AppColors.grey600 : Colors.grey;

    final filtered = quizzes == null
        ? <QuizSummaryModel>[]
        : (level == null
            ? quizzes!
            : quizzes!.where((q) => q.level == level).toList());

    return Scaffold(
      appBar: AppBar(
        title: Text('Quiz ${level != null ? " - ${level!.capitalize}" : ""}'),
        backgroundColor: primaryColor,
        foregroundColor: colorScheme.onPrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: filtered.isEmpty
            ? _buildEmptyState(context, greyColor, colorScheme)
            : ListView.separated(
                itemCount: filtered.length,
                separatorBuilder: (_, __) => const SizedBox(height: 8),
                itemBuilder: (context, index) {
                  final q = filtered[index];
                  return Card(
                    color: colorScheme.surface,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                    child: ListTile(
                      title: Text(
                        q.title,
                        style: TextStyle(color: colorScheme.onSurface),
                      ),
                      subtitle: Text(
                        'Questions: ${q.questionCount}',
                        style: TextStyle(
                          color: colorScheme.onSurface.withOpacity(0.6),
                        ),
                      ),
                      trailing: ElevatedButton(
                        onPressed: q.isAccessible
                            ? () => context.push('/quiz/${q.id}')
                            : null,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: primaryColor,
                          foregroundColor: colorScheme.onPrimary,
                        ),
                        child: Text(
                          q.isAccessible ? 'Commencer' : 'Bloqué',
                        ),
                      ),
                    ),
                  );
                },
              ),
      ),
    );
  }

  Widget _buildEmptyState(
      BuildContext context, Color greyColor, ColorScheme colorScheme) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.quiz_outlined,
              size: 100,
              color: greyColor,
            ),
            const SizedBox(height: 24),
            Text(
              'Aucun quiz disponible',
              style: context.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: colorScheme.onSurface,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              level != null
                  ? 'Aucun quiz trouvé pour le niveau "$level"'
                  : 'Cette catégorie ne contient pas encore de quiz',
              style: context.textTheme.bodyMedium?.copyWith(
                color: colorScheme.onSurface.withOpacity(0.6),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () {
                context.go('/home');
              },
              icon: const Icon(Icons.home),
              label: const Text('Retour à l\'accueil'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 16,
                ),
              ),
            ),
            const SizedBox(height: 16),
            OutlinedButton.icon(
              onPressed: () {
                context.pop();
              },
              icon: const Icon(Icons.category),
              label: const Text('Retour aux détails de la catégorie'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
